import sys
sys.path.append('../')

import json
# sys.path.append(r"E:\Learning\undergraduate\2021 Fall\CS397\Educational-website-and-courses-finder-for-keyword\code")
import webpage_crawler, rf_classifier

from  demo_kws import demo_kws
from website_db_connect import db
from tqdm import tqdm

import time
import math
import threading


def get_educ_urls(keyword, website_num=10, apply_filter=1):
    output = []
    output_ranking = []

    # keyword = input("Please enter your search keyword:")

    # website_num = int(input("Please enter your expected number(integer) of search results:"))

    # apply_filter = int(input("Do you want to apply the filter to clear similar results?(1 for yes, 0 for no)"))


    if (apply_filter != 0) and (apply_filter != 1):
        print("Please enter 0 or 1!")
        apply_filter = int(input("Do you want to apply the filter to clear similar results?(1 for yes, 0 for no)"))

    # user_header = input("Please enter the 'User-Agent' of your computer:")

    # print("Program is collecting search results, please wait...")

    user_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"

    # user_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    
    websites, features = webpage_crawler.DataSearch(keyword, website_num, apply_filter, user_header=user_header)

    # print(features)
    # print("Program is applying to classifier, please wait...")
    predicted_labels = rf_classifier.predict_for_user(features)
    # print(predicted_labels)

    # print("Program is generating outputs, please wait...")
    for i in range(len(predicted_labels[0])):
        if predicted_labels[0][i] == 2:
            output.append(websites[i])
            output_ranking.append(2)

    for i in range(len(predicted_labels[0])):
        if predicted_labels[0][i] == 1:
            output.append(websites[i])
            output_ranking.append(1)

    for i in range(len(predicted_labels[0])):
        if predicted_labels[0][i] == 0:
            output.append(websites[i])
            output_ranking.append(0)


    res = []
    for i in range(len(output)):
        if output_ranking[i] > 0:
            res.append(output[i])

    return res

def precompute_all(thread_id, num_workers, keyword_ts, pbar):
    """
        Filters educational websites / tutorials from Google search results for all keywords and stores them in the keyword_pages.tutorial table
    """
    cur = db.cursor()
    num_complete = 0


    for i in range(thread_id, len(keyword_ts), num_workers):
        kw_id, keyword = keyword_ts[i]
        # print(keyword)

        try:
            res = get_educ_urls(keyword)
            time.sleep(10)
        except Exception as e:
            print("Skipping keyword", keyword)
            print(e)
            continue

        if len(res) > 0:
            # print(json.dumps(res, indent=4))
            # print('-' * 12)
            for url in res:
                cur.execute(
                    """
                        INSERT INTO tutorial 
                        (keyword_id, url) 
                        VALUES 
                        (%s, %s)
                    """, 
                    [
                        kw_id,
                        url
                    ]
                )

            db.commit()

        num_complete += 1
        pbar.update(1)


        # if num_complete >= 4:
        #     break

        # if num_complete % 100 == 0:
        #     db.commit()
            # pass

    # db.commit()
    pbar.close()

def parallel_precompute(worker_idx, num_workers, num_threads=3):
    threads = []
    cur = db.cursor()

    # cur.execute("SELECT id, name FROM keyword ORDER BY id")
    cur.execute(f"""
        SELECT id, name 
        FROM keyword 

        WHERE name IN ({",".join(['%s'] * len(demo_kws))})
        ORDER BY id
        """, demo_kws)

    keyword_ts = cur.fetchall()
    print(keyword_ts, len(keyword_ts))
    # return
    
    # Split work among several machines
    chunk_size = math.ceil(len(keyword_ts) / num_workers)
    start_idx = chunk_size * worker_idx
    keyword_ts = keyword_ts[start_idx: start_idx + chunk_size]

    pbar = tqdm(total=len(keyword_ts))

    # Start threads
    for i in range(num_threads):
        t = threading.Thread(target=precompute_all, args=(i, num_threads, keyword_ts, pbar))
        t.start()

        threads.append(t)

    print("Started threads. Waiting for worker threads....", file=sys.stderr)
    for t in threads:
        t.join()

    pbar.close()



if __name__ == '__main__':
    parallel_precompute(worker_idx=0, num_workers=1, num_threads=1)
    exit()

    keyword = sys.argv[1]
    website_num = int(sys.argv[2])
    apply_filter = int(sys.argv[3])

    res = get_educ_urls(keyword, website_num, apply_filter)
    print(json.dumps(res))

# print(
#     "Note: The output websites will be sorted and contained in a list, with the leftmost being most useful and rightmost being least useful")
# print("The outputs are as followed:", output)
# print("Useful level(larger = better):",output_ranking)
