from omega.node.ProofOfStake import ProofOfStake
from omega.node.Lot import Lot
import string
from tqdm import tqdm
import random


def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString


if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update('bob', 100)
    pos.update('alice', 100)

    for _ in range(10):
        bobWins = 0
        aliceWins = 0
        for i in tqdm(range(100)):
            forger = pos.forger(getRandomString(i))
            if forger == 'bob':
                bobWins += 1
            elif forger == 'alice':
                aliceWins += 1
            else:
                print(forger)

        print('Bob won: ' + str(bobWins) + ' times')
        print('Alice won: ' + str(aliceWins) + ' times')
