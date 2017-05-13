# -*- coding: utf-8 -*-
"""
Support functions for reference parsing
"""
__author__ = """Giovanni Colavizza"""

from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.metrics import make_scorer, accuracy_score, classification_report
from sklearn_crfsuite import metrics
import statistics

#
# BALANCED ERROR RATE calculations (a cost function for skewed datasets)
#
def BER(yn, ynhat):
    """
    Implementation of Balanced Error Rate

    :param yn: ground truth
    :param ynhat: predicted values
    :return: error score

    """
    y = list()
    for z in yn:
        y.extend(z)
    yhat = list()
    for z in ynhat:
        yhat.extend(z)
    yn = np.array(y)
    ynhat = np.array(yhat)
    c = set(list(yn) + list(ynhat)) # set of unique classes
    error = 0.0
    numClasses = 0
    for C in c:
        if(len(np.array(yn == C)) != 0):
            error += np.sum(np.array(yn == C) * np.array(yn != ynhat))/float(np.sum(np.array(yn == C)))
            numClasses += 1
    if numClasses == 0: return 1.0
    error = error/numClasses
    return error

def BER_vector(yn, ynhat):
    """
    Implementation of Balanced Error Rate, returns a vector with errors for each class

    :param yn: ground truth
    :param ynhat: predicted values
    :return: error score vector, scores for each class

    """
    y = list()
    for z in yn:
        y.extend(z)
    yhat = list()
    for z in ynhat:
        yhat.extend(z)
    yn = np.array(y)
    ynhat = np.array(yhat)
    c = set(list(yn) + list(ynhat)) # set of unique classes
    error = list()
    classes = list()
    for C in c:
        if(np.sum(np.array(yn == C)) != 0):
            error.append(np.sum(np.array(yn == C) * np.array(yn != ynhat))/float(np.sum(np.array(yn == C))))
            classes.append(C)
    return error, classes

def error_report(yn, ynhat):
    """
    Helper function for error report.

    :param yn: ground truth labels
    :param ynhat: predicted labels
    :return: Print error report
    """
    print("Accuracy: ", accuracy_score(yn, ynhat))
    print("Report: ", classification_report(yn, ynhat))

    print("BER error: ", BER(yn,ynhat))
    print("BER class error: ", BER_vector(yn,ynhat))

def flatten_predictions(y):
    # Takes a list of list and returns a list

    y_n = list()
    for i in y:
        y_n.extend(i)
    return y_n

#
# PLOTTING
#
def plot_learning_curve(estimator, title, X, y, labels, ylim=None, cv=None,
                        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5), message=""):
    """
    FROM: http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html

    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    # Define scorer
    scorer = make_scorer(metrics.flat_f1_score, 
                        average='weighted', labels=labels)
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring=scorer)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Testing score")

    plt.legend(loc="best")
    #plt.savefig("plots/learning_curve_%s.pdf"%message)
    return plt

#
# EXPORTS
#
# Takes an annotated or not page and dumps it for the lookup
def parse_page(page):
    """
    Consolidates all the references parsed for a single page
    :param page: A page in a doc, with specific and BET tags
    :return: A list of consolidated references
    """

    refs = list()
    ref = dict()
    list_of_generic_tags = list()
    tag = ""
    tag_start = 0
    previous_end = 0
    surface = ""
    in_ref = False
    counter = 1
    continuation_candidate_out = False
    continuation_candidate_in = False
    first_ref = True
    for n,token in enumerate(page["offsets"]):
        if in_ref and n == len(page["offsets"]) -1:
            continuation_candidate_out = True # side end, page 1
        # check generic tag
        if (page["BET_tags"][n].startswith("b") or page["BET_tags"][n].startswith("i")) and not in_ref:
            in_ref = True
            if first_ref and page["BET_tags"][n].startswith("i"):
                continuation_candidate_in = True  # side in, page 2
                first_ref = False
            else:
                continuation_candidate_in = False
                first_ref = False
            generic = page["BET_tags"][n][2:]
            list_of_generic_tags = [generic]
            ref = {"reference_string": "", "continuation_candidate_out": continuation_candidate_out, "continuation_candidate_in": continuation_candidate_in,
                    "in_golden": page["is_annotated"], "ref_type": generic, "contents": OrderedDict(), "order_in_page": counter, "continuation": False}
            continuation_candidate_in = False
            surface = token[0][0]
            tag = page["specific_tags"][n]
            tag_start = token[0][1]
        elif page["BET_tags"][n].startswith("b") and in_ref: # maybe incorrect boundaries, we split nevertheless
            first_ref = False
            ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag":tag, "surface":surface,
                                                                    "start":tag_start,"end":previous_end,
                                                                    "single_page_file_number":int(page["single_page_file_number"]),
                                                                    "page_id":page["page_id"],
                                                                    "page_mongo_id": page["page_mongo_id"]}})
            ref["continuation_candidate_out"] = continuation_candidate_out
            try:
                ref["ref_type"] = statistics.mode(list_of_generic_tags)  # vote for most frequent generic tag
            except:
                pass # if mode not unique, just pick one
            # add final global surface
            ref["reference_string"] = " ".join([x["surface"] for x in ref["contents"].values()])
            refs.append(ref)
            counter += 1 # dumping
            # new ref starting
            generic = page["BET_tags"][n][2:]
            list_of_generic_tags = [generic]
            ref = {"reference_string": "", "continuation_candidate_out": continuation_candidate_out, "continuation_candidate_in": continuation_candidate_in,
                    "in_golden": page["is_annotated"], "ref_type": generic, "contents": OrderedDict(), "order_in_page": counter, "continuation": False}
            continuation_candidate_in = False
            surface = token[0][0]
            tag = page["specific_tags"][n]
            tag_start = token[0][1]
        elif page["BET_tags"][n].startswith("o") and in_ref: # DUMP if outside
            ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag": tag, "surface": surface,
                                                                      "start": tag_start, "end": previous_end,
                                                                      "single_page_file_number": int(
                                                                          page["single_page_file_number"]),
                                                                      "page_id": page["page_id"],
                                                                      "page_mongo_id": page["page_mongo_id"]}})
            ref["continuation_candidate_out"] = continuation_candidate_out
            try:
                ref["ref_type"] = statistics.mode(list_of_generic_tags)  # vote for most frequent generic tag
            except:
                pass # if mode not unique, just pick one
            # add final global surface
            ref["reference_string"] = " ".join([x["surface"] for x in ref["contents"].values()])
            refs.append(ref)
            counter += 1  # dumping
            in_ref = False
        elif page["BET_tags"][n].startswith("e") and in_ref: #DUMP if end
            list_of_generic_tags.append(page["BET_tags"][n][2:])
            if page["specific_tags"][n] != tag:
                # dump ref before and create a new one
                ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag": tag, "surface": surface,
                                                                          "start": tag_start, "end": previous_end,
                                                                          "single_page_file_number": int(page["single_page_file_number"]),
                                                                          "page_id": page["page_id"],
                                                                      "page_mongo_id": page["page_mongo_id"]}})
                ref["continuation_candidate_out"] = continuation_candidate_out
                tag = page["specific_tags"][n]
                surface = token[0][0]
                tag_start = token[0][1]
                ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag": tag, "surface": surface,
                                                                          "start": tag_start, "end": token[0][2],
                                                                          "single_page_file_number": int(page["single_page_file_number"]),
                                                                          "page_id": page["page_id"],
                                                                      "page_mongo_id": page["page_mongo_id"]}})
                ref["continuation_candidate_out"] = continuation_candidate_out
            else:
                # update ref before and dump it
                surface = surface+" "+token[0][0]
                ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag": tag, "surface": surface,
                                                                          "start": tag_start, "end": token[0][2],
                                                                          "single_page_file_number": int(
                                                                              page["single_page_file_number"]),
                                                                          "page_id": page["page_id"],
                                                                      "page_mongo_id": page["page_mongo_id"]}})
                ref["continuation_candidate_out"] = continuation_candidate_out
            # dump full reference
            try:
                ref["ref_type"] = statistics.mode(list_of_generic_tags)  # vote for most frequent generic tag
            except:
                pass # if mode not unique, just pick one
            # add final global surface
            ref["reference_string"] = " ".join([x["surface"] for x in ref["contents"].values()])
            refs.append(ref)
            counter += 1 # dumping
            in_ref = False
        elif in_ref:
            list_of_generic_tags.append(page["BET_tags"][n][2:])
            if page["specific_tags"][n] != tag and len(page["specific_tags"][n]) > 0:
                # dump ref before and create a new one
                ref["contents"].update({str(len(ref["contents"].keys())+1): {"tag": tag, "surface": surface,
                                                                          "start": tag_start, "end": previous_end,
                                                                          "single_page_file_number": int(
                                                                              page["single_page_file_number"]),
                                                                          "page_id": page["page_id"],
                                                                      "page_mongo_id": page["page_mongo_id"]}})
                ref["continuation_candidate_out"] = continuation_candidate_out
                tag = page["specific_tags"][n]
                surface = token[0][0]
                tag_start = token[0][1]
            else:
                # update surface before
                surface = surface+" "+token[0][0]
        previous_end = token[0][2]
            
    return refs

# dump all annotated references to json, consolidating continuations
def process_doc(doc):
    """
    Process a single doc

    :param doc: A doc from parsing
    :return: The same doc with all its references consolidated, and a list of possible continuations for that doc. A doc is an issue or a bid/monograph (i.e. single volume)
    """

    doc["references"] = list()
    possible_continuations = list()
    for page in doc["pages"].values():
        doc["references"].extend(parse_page(page))
    # process continuations
    cont_refs_out = [(n,x) for n,x in enumerate(doc["references"]) if x["continuation_candidate_out"]]
    cont_refs_in = [(n,x) for n,x in enumerate(doc["references"]) if x["continuation_candidate_in"]]
    for r_out in cont_refs_out:
        if len(r_out[1]["contents"].keys()) < 1:
            continue
        for r_in in cont_refs_in:
            if len(r_in[1]["contents"].keys()) < 1:
                continue
            try:
                if (r_out[1]["contents"]['1']["single_page_file_number"] == r_in[1]["contents"]['1']["single_page_file_number"] -1) and r_out[1]["ref_type"] == r_in[1]["ref_type"] and not r_out[1]["contents"][str(len(r_out[1]["contents"].keys()))]["tag"] == "pagination":
                    # MERGE
                    prev_len = len(r_out[1]["contents"].keys())
                    for n,token in list(r_in[1]["contents"].items()):
                        doc["references"][r_out[0]]["contents"].update({str(prev_len+int(n)+1): token})
                    doc["references"][r_out[0]]["continuation"] = True
                    del doc["references"][r_in[0]]
                    possible_continuations.append((r_out,r_in))
            except:
                pass # skip merging if problems arise

    return doc, possible_continuations

from multiprocessing import Pool
from datetime import datetime
def json_outputter(data,threads=7):
    """
    Exports a json-like version of the consolidated, parsed references
    :param data: parsed data
    :param threads: number of threads to use
    :return: list of refs per doc, list of refs, list of consolidations
    """

    threads = Pool(threads)
    data_json = list()
    data_json_references = list()
    pc_list = list()
    for doc, pc in threads.imap_unordered(process_doc, data):
        data_json.append(doc)
        pc_list.extend(pc)
        for reference in doc["references"]:
            reference["bid"] = doc["bid"]
            reference["issue"] = doc["doc_number"]
            reference["updated_at"] = datetime.now()
            data_json_references.append(reference)
    return data_json, data_json_references, pc_list
