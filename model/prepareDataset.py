import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import Levenshtein  # Install the Levenshtein package using pip


with open("../data/domainModel/domainPhishingPredictor/qualifiedTLDs.txt", "r") as file:
    TLDs = file.readlines()


def shrinkDataset(filename, sample_size):
    import pandas as pd

    # Read the large dataset of good domains from the original CSV file in chunks
    chunk_size = 10000  # Adjust the chunk size as per your resource limitations

    # Initialize an empty DataFrame to store the sampled data
    sampled_data = pd.DataFrame()

    # Iterate through the chunks of data
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # Sample a subset from the current chunk
        subset = chunk.sample(n=min(sample_size, len(chunk)), random_state=42)

        # Concatenate the sampled subset to the overall sampled data
        sampled_data = pd.concat([sampled_data, subset], ignore_index=True)

        # Break the loop if the desired sample size is reached
        if len(sampled_data) >= sample_size:
            break

    # Save the sampled data to a new CSV file
    return sampled_data

def remove_parameters(link):
    link = link.replace("https://", '')
    link = link.replace("http://", '')
    link = link.split("/")[0]
    return link

def prepare_bad_urls(filename):
    df = pd.read_excel(filename)
    bad_urls = df.iloc[:, 0]
    bad_urls = bad_urls.rename('Domain')
    bad_urls_df = pd.DataFrame(columns=["Domain", "isPhishing"])
    bad_urls_df["Domain"] = bad_urls
    bad_urls_df["isPhishing"] = True
    return bad_urls_df

def prepare_good_urls(filename):
    df = pd.read_csv(filename)
    good_urls = df['domain'].dropna()
    good_urls_df = pd.DataFrame(columns=["Domain", "isPhishing"])
    good_urls_df["Domain"] = good_urls
    good_urls_df["isPhishing"] = False
    return good_urls_df

def add_SSL(row):
    #check whether it was taken from actual companies dataset. Then, we assume that everything was ok
    if(not row["isPhishing"]):
        return True
    #the actual check
    if ("https" in row["Domain"]):
        return True
    elif ("http" in row["Domain"]):
        return False

def add_length(domain):
    return len(domain)

def add_subdomains_number(domain):
    return len(domain.split("."))

def add_hasQualifiedTLD(domain):
    subdomains = domain.split(".")
    for tld in TLDs:
        if tld in subdomains:
            return True
    return False

original_domains = prepare_good_urls("../data/domainModel/domainPhishingPredictor/good_urls_smaller.csv")["Domain"].tolist()
def add_isTyposquatted(url, threshold=2):
    """
    Checks whether a given URL is typosquatted or not.

    Args:
        url (str): The URL to check.
        original_domains (list): A list of original domain names.
        threshold (int): The maximum Levenshtein distance allowed for a potential typosquatting match.

    Returns:
        bool: True if the URL is potentially typosquatted, False otherwise.
    """

    for original_domain in original_domains:
        url = url.split(".")[0]
        original_domain = original_domain.split(".")[0]
        distance = Levenshtein.distance(url, original_domain)
        if ((distance <= threshold) and (distance != 0)) and (len(url) > 7):
            print(url, original_domain, distance)
            return True
    return False


def add_features(df):
    # Add SSL
    #if it has https we set hasSSL to True
    df["hasSSL"] = df.apply(add_SSL, axis=1)

    #Remove http and https from domains
    df["Domain"] = df["Domain"].apply(remove_parameters)

    #Add length
    df["Length"] = df["Domain"].apply(add_length)

    #Add subdomains number
    df["SubdomainsNum"] = df["Domain"].apply(add_subdomains_number)

    #Add tld check
    df["hasQualifiedTLD"] = df["Domain"].apply(add_hasQualifiedTLD)

    # Add isTypoSquated
    # df["isTypoSquated"] = df["Domain"].apply(add_isTyposquatted)


# bad_urls = prepare_bad_urls('../data/domainModel/FalszyweInwestycjeUrle.xlsx')
# good_urls = prepare_good_urls("../data/domainModel/companies_sorted.csv")
# joinAndLabel(bad_urls)
# shrinked = shrinkDataset("../data/domainModel/companies_sorted.csv", 18233)
# shrinked.to_csv("../data/domainModel/good_urls_smaller.csv", index=False)

bad_urls = prepare_bad_urls("../data/domainModel/domainPhishingPredictor/FalszyweInwestycjeUrle.xlsx")
good_urls = prepare_good_urls("../data/domainModel/domainPhishingPredictor/good_urls_smaller.csv")
dataset = pd.concat([bad_urls, good_urls], ignore_index=True)
add_features(dataset)
corr = dataset.drop("Domain", axis=1).corr()
print(corr["isPhishing"])

# X: features, y: target variable
X = dataset.drop(["Domain", "isPhishing"], axis=1)
y = dataset["isPhishing"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train)
sgd_cls = SGDClassifier(loss="log_loss", random_state=42)
sgd_cls.fit(X_train, y_train)
y_pred = sgd_cls.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)