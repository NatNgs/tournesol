"""
Module containting the ml_run() function used in ml_train.py
between fetch_data() and save_data()
"""
import os
import logging
from time import time
import gin

from ml.licchavi import Licchavi
from ml.handle_data import (
    select_criteria, shape_data, distribute_data,
    distribute_data_from_save, format_out_loc, format_out_glob)


TOURNESOL_DEV = bool(int(os.environ.get("TOURNESOL_DEV", 0)))  # dev mode
ML_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
HP_PATH = ML_DIR + 'hyperparameters.gin'
FOLDER_PATH = ML_DIR + 'checkpoints/'
FILENAME = "models_weights"
PATH = FOLDER_PATH + FILENAME
os.makedirs(FOLDER_PATH, exist_ok=True)
logging.basicConfig(filename=ML_DIR + 'ml_logs.log', level=logging.INFO)


def _get_licchavi(
        nb_vids, vid_vidx, criteria,
        device, verb, ground_truths, licchavi_class):
    """ Used to decide wether to use Licchavi() or LicchaviDev() class

    nb_vids (int): number of videos
    vid_vidx (dictionnary): dictionnary of {video ID: video index}
    criteria (str): comparison criteria learnt
    device (str): device used (cpu/gpu)
    ground_truths (float array, couples list list, float array)
    verb (float): verbosity level
    global, local and s parmaeters ground truths (test mode only)
    licchavi_class (Licchavi()): training structure used
                                        (Licchavi or LicchaviDev)

    Returns:
        (Licchavi()): Licchavi or LicchaviDev object
    """
    if licchavi_class == Licchavi:
        return Licchavi(
            nb_vids, vid_vidx, criteria, verb=verb)
    # only in dev mode
    test_mode = ground_truths is not None
    licch = licchavi_class(
        nb_vids, vid_vidx, criteria, test_mode, device, verb)
    if test_mode:
        licch.set_ground_truths(*ground_truths)
    return licch


def _set_licchavi(
        comparison_data, criteria,
        fullpath=None, resume=False,
        verb=2, device='cpu',
        ground_truths=None, licchavi_class=Licchavi):
    """ Shapes data and inputs it in Licchavi to initialize

    comparison_data (list of lists): output of fetch_data()
    criteria (str): rating criteria
    fullpath (str): path from which to load previous training
    resume (bool): wether to resume previous training or not
    verb (int): verbosity level
    device (str): device used (cpu/gpu)
    ground_truths (float array, couples list list, float array):
        global, local and s parmaeters ground truths (test mode only)
    licchavi_class (Licchavi()): training structure used
                                        (Licchavi or LicchaviDev)

    Returns :
        (Licchavi()): Licchavi object initialized with data
        (int array): array of users IDs in order
    """
    # shape data
    one_crit_data = select_criteria(comparison_data, criteria)
    if len(one_crit_data) == 0:  # if no data for selected criteria
        logging.warning(f"No comparison for this criteria ({criteria})")
        return None, None
    full_data = shape_data(one_crit_data)
    # set licchavi using data
    if resume:
        nodes_dic, users_ids, vid_vidx = distribute_data_from_save(full_data,
                                                                   fullpath,
                                                                   device)
        licch = _get_licchavi(
            len(vid_vidx), vid_vidx, criteria,
            device, verb, ground_truths, licchavi_class
        )
        licch.load_and_update(nodes_dic, users_ids, fullpath)
    else:
        nodes_dic, users_ids, vid_vidx = distribute_data(full_data, device)
        licch = _get_licchavi(
            len(vid_vidx), vid_vidx, criteria,
            device, verb, ground_truths, licchavi_class
        )
        licch.set_allnodes(nodes_dic, users_ids)
    return licch, users_ids  # FIXME we can do without users_ids ?


def _train_predict(
        licch, epochs_loc, epochs_glob,
        fullpath=None, save=False, compute_uncertainty=False):
    """ Trains models and returns video scores for one criteria

    licch (Licchavi()): licchavi object innitialized with data
    epochs_loc (int): number of local epochs of gradient descent for Licchavi
    epochs_glob (int): number of global epochs of gradient descent for Licchavi
    fullpath (str): path where to save trained models
    save (bool): wether to save the result of training or not
    verb (int): verbosity level
    compute_uncertainty (bool): wether to compute uncertainty or not (slow)

    Returns :
    - (list of all vIDS , tensor of global video scores)
    - (list of arrays of local vIDs , list of tensors of local video scores)
    (float list list, float list): uncertainty of local scores,
                                    uncertainty of global scores
                                    (None, None) if not computed
    """
    uncert_loc = licch.train_loc(
        epochs_loc, compute_uncertainty=compute_uncertainty
    )
    uncert_glob = licch.train_glob(
        epochs_glob, compute_uncertainty=compute_uncertainty
    )
    uncertainties = (uncert_loc, uncert_glob)
    glob, loc = licch.output_scores()
    if save:
        licch.save_models(fullpath)
    return glob, loc, uncertainties


@gin.configurable
def ml_run(
        comparison_data,
        epochs_loc_full, epochs_glob_full, epochs_loc_res, epochs_glob_res,
        criterias,
        resume=False, save=True, verb=1, device='cpu', ground_truths=None,
        compute_uncertainty=False, licchavi_class=Licchavi):
    """ Runs the ml algorithm for all criterias

    comparison_data (list of lists): output of fetch_data()
    epochs_loc_full (int): number of local epochs of
        gradient descent for Licchavi (from scratch)
    epochs_glob_full (int): number of global epochs of
        gradient descent for Licchavi (from scratch)
    epochs_loc_res (int): number of local epochs of
        gradient descent for Licchavi (from save)
    epochs_glob_res (int): number of global epochs of
        gradient descent for Licchavi (from save)
    criterias (str list): list of criterias to compute
    resume (bool): wether to resume from save or not
    save (bool): wether to save result of training or not
    verb (int): verbosity level
    device (str): device used (cpu/gpu)
    ground_truths (float array, couples list list, float array):
        global, local and s parmaeters ground truths (test mode only)
    compute_uncertainty (bool): wether to compute uncertainty or not (slow)
    licchavi_class (Licchavi()): training structure used
                                        (Licchavi or LicchaviDev)

    Returns:
        (list list): list of [video_id: int, criteria_name: str,
                                score: float, uncertainty: float]
        (list list): list of
        [   contributor_id: int, video_id: int, criteria_name: str,
            score: float, uncertainty: float]
    """  # FIXME: not better to regroup contributors in same list or smthg ?
    ml_run_time = time()
    epochs_loc = epochs_loc_res if resume else epochs_loc_full
    epochs_glob = epochs_glob_res if resume else epochs_glob_full
    glob_scores, loc_scores = [], []

    for criteria in criterias:
        logging.info('PROCESSING %s', criteria)
        fullpath = PATH + '_' + criteria

        # preparing data
        licch, users_ids = _set_licchavi(
            comparison_data, criteria,
            fullpath, resume, verb, device,
            ground_truths, licchavi_class=licchavi_class
        )

        if licch is not None:  # if not 0 data for selected criteria

            # training and predicting
            glob, loc, uncertainties = _train_predict(
                licch, epochs_loc, epochs_glob, fullpath, save,
                compute_uncertainty=compute_uncertainty
            )
        # putting in required shape for output
        out_loc = format_out_loc(loc, users_ids, criteria, uncertainties[0])
        out_glob = format_out_glob(glob, criteria, uncertainties[1])
        loc_scores += out_loc
        glob_scores += out_glob

    logging.info('ml_run() total time : %s', round(time() - ml_run_time))
    if TOURNESOL_DEV:  # return more information in dev mode
        return glob_scores, loc_scores, (licch, glob, loc, uncertainties)
    return glob_scores, loc_scores
