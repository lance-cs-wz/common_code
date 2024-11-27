# -*- coding:utf-8 -*-
# Python version is 2.7
import os
import re
import sys
import json
import time

import logging
import logging.config

logging.config.fileConfig("./logging_config.ini")
log = logging.getLogger()

import get_order
import update_ans_pic
import add_item_new_solution
import get_num_iid_data

now_time_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def usage():
    sys.stderr.write("usage:\n")
    sys.stderr.write("  python2.7 %s in_file out_file\n" % sys.argv[0])


def get_post_result(method, request_data_str):
    data = {}
    result = 100
    message = "bad method"

    request_data_dict = json.loads(request_data_str)

    if method == "getOrder":
        reload(get_order)
        if "id" in request_data_dict:
            id = request_data_dict["id"]
            data = get_order.get_order_num_iids(id)
        message = "Done getOrder"

    if method == "updateAnsPic":
        reload(update_ans_pic)
        if "picFile" in request_data_dict:
            pic_file = request_data_dict["picFile"]
            data = update_ans_pic.change_output_format(update_ans_pic.update_ans_pic(pic_file))
        message = "Done updateAnsPic"

    if method == "getNumIidData":
        reload(get_num_iid_data)
        if "numIid" in request_data_dict:
            num_iid = request_data_dict["numIid"]
            data = get_num_iid_data.get_num_iid_data(num_iid)
        message = "Done getNumIidData"

    if method == "addItemNewSolution":
        reload(add_item_new_solution)
            
        knowledge_id = 0
        if "knowledgeId" in request_data_dict:
            knowledge_id = request_data_dict["knowledgeId"]

        seller_id = 0
        if "sellerId" in request_data_dict:
            seller_id = request_data_dict["sellerId"]

        num_iid = 0
        if "numIid" in request_data_dict:
            num_iid = request_data_dict["numIid"]

        seller_nick = ""
        if "sellerNick" in request_data_dict:
            seller_nick = request_data_dict["sellerNick"]

        solution = ""
        if "solution" in request_data_dict:
            solution = request_data_dict["solution"]

        ans_pic_url = ""
        if "ansPicUrl" in request_data_dict:
            ans_pic_url = request_data_dict["ansPicUrl"]

        data = add_item_new_solution.add_item_new_solution(
                knowledge_id, seller_id, seller_nick, solution, ans_pic_url, num_iid)

        message = "Done addItemNewSolution"

    return data, result, message

                
if __name__ == "__main__":
    get_post_result("getOrder", '{"id": 1}')
    get_post_result("updateAnsPic", '{"picFile": ""}')
    get_post_result("addItemNewSolution", '{"ansPicUrl": "", \
            "knowledgeId": 0, "numIid": 23, "sellerId": 11, "sellerNick": \
            "seller_11", "solution": "这是一个测试用的答案"}')
    get_post_result("getNumIidData", '{"numIid": 571688607793}')
