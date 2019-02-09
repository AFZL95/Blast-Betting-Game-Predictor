import hashlib
import hmac
import csv
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor


def getPrevHash(currHash):
    prevHash = hashlib.sha256()
    prevHash.update(currHash)
    return prevHash.hexdigest().encode("utf-8")

# implemented dynamically for any assumable divider ("mod" parameter)


def hmac_sum_calculator(hmac_hash):
    # temporary variable for...
    sum = 0
    # check if it's divisible by 4
    o = len(hmac_hash) % 4

    # indexer for our 16 number of 4 character parts of SHA-256
    i = o - 4 if o > 0 else 0

    print(hmac_hash)
    cnt_of_parts = 1
    while i < len(hmac_hash):
        dec_eq_of_each_part = int(currHash[i: i + 4], 16)
        print("{0} Part: {1} ".format(cnt_of_parts, currHash[i:i + 4]) + "| Dec.eq: {0}".format(dec_eq_of_each_part))

        # val = ((val << 16) + int(hmacHash[i: i + 4], 16)) % mod
        # calculating the decimal sum of all 16 values
        sum += int(hmac_hash[i: i + 4], 16)

        # counting up the counters
        i += 4
        cnt_of_parts += 1
    return sum


# calculate blast coefficient from the given sha256
def calculate_blast_from_hash(currHash):
    # creating a HMAC object from the given sha1 string besides of specifying length of the encryption
    # HMAC stands for (hash message authentication code)
    hmac_calculator = hmac.new(currHash, digestmod=hashlib.sha256)

    # if we have found the constant pattern of generating SHA-256's...
    # we can use this in order to create future permutations
    # hmac_calculator.update(b"000000000000000007a9a31ff7f07463d91af6b5454241d5faf282e5e0fe1b3a")

    hmac_hash_instance = hmac_calculator.hexdigest().encode("utf-8").decode()

    # in the case of sum of desired parts dividable by 50 "calculate_blast_from_hash" will return zero
    # a.k.a "U Lose Dude!"
    if hmac_sum_calculator(hmac_hash_instance) % 50 == 0:
        return 0
    h = int(hmac_hash_instance[0: 13], 16)
    e = math.pow(2, 52)
    return (math.floor((100 * e - h) / (e - h)) / 100)


# main thing goes from here
# preaparing the approximation
limit = 100
gameHash = input("Please enter a game hash to start with: ").encode("utf-8")
print("Writing past crashes to 'crashes.txt'...")
currHash = gameHash
outputFile = open(os.path.join(os.path.dirname(__file__), "crashes.csv"), "w")
csvWriter = csv.writer(outputFile)
csvWriter.writerow(["Game Hash", "Crash"])

for i in range(limit):
    csvWriter.writerow([currHash.decode(), str(calculate_blast_from_hash(currHash))])
    currHash = getPrevHash(currHash)
outputFile.close()
print("Write complete!")

crashes = pd.read_csv(os.path.join(os.path.dirname(__file__), "crashes.csv"))
crashes = crashes.query("Crash < 10")
crashes = crashes.assign(Time=list(range(len(crashes))), Normalized_Crash=crashes["Crash"].apply(np.floor))

regressor = KNeighborsRegressor(n_neighbors=20)
attributes = crashes["Time"].values.reshape(-1, 1)
labels = crashes["Crash"]
train_x = attributes[:-44000]
test_x = attributes[-44000:]
train_y = labels[:-44000]
test_y = labels[-44000:]
regressor.fit(train_x, train_y)
prediction = regressor.predict(test_x)
print(prediction)
plt.scatter(test_x, test_y, color="black")
plt.plot(test_x, prediction, color="blue", linewidth=3)
plt.show()


#currHash = "05a97ac68ba582d0a7f67a5ffb62743cefe7cc015122929ad0153282ebd140ca"