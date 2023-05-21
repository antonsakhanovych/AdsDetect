import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# 1 - spam, 0 - ad

def replace_status(Status):
    if Status == "spam": return 1
    elif Status == "ad": return 0

spam_df = pd.read_csv("../data/spamNotSpamModel/spam.csv")
ads_df = pd.read_csv("../data/spamNotSpamModel/ads.csv")

spam = spam_df.loc[spam_df["Status"] == "spam"]
spam = spam.drop(['non1', 'non2'], axis=1)
df = pd.concat([spam, ads_df], ignore_index=True)
df = df.drop("Unnamed: 4", axis=1)
df["Status"] = df["Status"].apply(replace_status)

df_x = df["Text"]
df_y = df["Status"]
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, train_size=0.2, random_state=42)
cv = CountVectorizer()
X_train_cv = cv.fit_transform(X_train)

mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train_cv, y_train)

X_test_cv = cv.transform(X_test)
accuracy = mnb_classifier.score(X_test_cv, y_test)
# print("Accuracy:", accuracy)

def isSpamOrAd(text):
    text = [text]
    test_cv = cv.transform(text)
    result = mnb_classifier.predict(test_cv)
    if result == [0]: return "Ad"
    else: return "Spam"