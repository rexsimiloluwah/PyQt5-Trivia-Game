import os 
import yaml
import requests 
from requests.exceptions import HTTPError

BASE_URL = "https://opentdb.com"

def format_text(text):
    formatting = [
        ("&#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">"),
        ("&amp;", "&")
    ]

    for t in formatting:
        text=text.replace(t[0], t[1])
    return text

def fetch_questions(category=9, amount=30, difficulty="medium", type="multiple"):
    """ Fetches questions for any category from the Opentdb API """
    URL = f"{BASE_URL}/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={type}"
    response = requests.get(URL)
    if response.status_code == 200:
        results = response.json()['results']
        results = map(lambda x: {
            "question": format_text(x["question"]),
            "correct_answer": format_text(str(x["correct_answer"])),
            "options": list(map(lambda x: format_text(x), x["incorrect_answers"]+[x["correct_answer"]])),
            }, results)
        return list(results)
    else:
        return []

def save_categories():
    """ Saves the fetched questions to a .yaml file for each category """
    URL = f"{BASE_URL}/api_category.php"

    try:
        response = requests.get(URL)
        if (response.status_code == 200):
            results = response.json()['trivia_categories']
            with open(os.path.join('assets','categories.yaml'), 'w') as f:
                categories = yaml.dump(results, f)
    except HTTPError as e:
        raise e

def fetch_categories():
    """ Fectches the trivia categories """
    with open(os.path.join('assets','categories.yaml')) as f:
        categories = yaml.full_load(f)
        #print(categories)
        categories = {category["name"]:category["id"] for category in categories}
        return categories

def fetch_and_save_questions():
    """ Fetches and saves questions in a .yaml file locally """
    if not os.path.isdir("questions"):
        os.mkdir("questions")

    categories = fetch_categories()
    difficulties = ['easy','medium','hard']
    for cat_id in categories.values():
        try:
            questions = {d:[] for d in difficulties} 
            for d in difficulties:
                fetched_questions = fetch_questions(category=cat_id, amount=40, difficulty=d)
                questions[d] = fetched_questions 
            with open(os.path.join("questions", f"{str(cat_id)}.yaml"), "w") as file:
                documents = yaml.dump(questions, file)
            print(f"[COMPLETED]: Fetched questions for category: {cat_id}")
        except Exception as e:
            raise(e)

def fetch_questions_local(category_id=9, amount=30, difficulty="easy", type="multiple"):
    """ Fetches questions from the local .yaml files for each category """
    file_path = os.path.join("questions",f"{category_id}.yaml")
    try:
        with open(file_path, "r") as file:
            full_questions = yaml.full_load(file)
            questions = full_questions[difficulty][:amount]
        return questions 
    except:
        return None

if __name__ == '__main__':
    # print("Working")
    fetch_and_save_questions()
    #print(fetch_questions_local())
