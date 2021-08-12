import pickle
import requests
import os

class Session:
    def __init__(self) -> None:
        pass

    def load_session(self, file_name) -> requests.Session or None:
        # Load/Create the session 
        if os.path.isfile('{}.pkl'.format(file_name)) is True:
            with open('{}.pkl'.format(file_name), 'rb') as f: 
                reqs = pickle.load(f)
                return reqs
        else:
            return None
    
    def save_session(self, reqs, file_name) -> None:
        # Persist the session through program runs 
        with open('{}.pkl'.format(file_name), 'wb') as f: 
            pickle.dump(reqs, f)
        return None