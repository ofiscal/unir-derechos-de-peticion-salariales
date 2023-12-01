import os


agency_root = "data/input/agency_responses"

with open('.git/HEAD') as f:
  head = f.read() [5:-1] # drop the leading "refs: " and trailing "\n".
with open('.git/' + head) as f:
  latest_commit = f.read() [:-1] # drop the trailing "\n"
del(head)

if not os.path.exists ( "pickles/" + latest_commit ):
  os.makedirs (         "pickles/" + latest_commit )

latest_pickle_path = os.path.join ( "pickles",
                                    latest_commit, )
