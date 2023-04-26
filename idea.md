# Idea

## Problem Definition

When users want to access some private data on a web service they need to authenticate themselves. This is the process by which a user confirms to the service their identity in order to access sensitive data. Authentication is done either through something a user knows, has, or is.

Unfortunately, humans are prone to error. People will often reuse passwords or password fragments. Additionally, they are prone to entering data into malicious services. This means that phishing is still highly successful and prevalent.

Moreover, small websites are sometimes (though less commonly in the past) poorly designed. Not all companies abide by secure standards to store user data such as usernames and passwords. Worse, it can be impossible to verify such practices.

The solution then is two-fold. First, websites must be required to authenticate themselves to users and second, there must be some cost to attempting a log-in (this cost must not necessarily be irrevokable).

## Steps

Step 1: To authenticate

Send to blockchain to verify: 

Website has to sign "own_name+user_account_id+current_token"

sends json {name: own_name,  signature: signed_str}

if signature is valid:
    blockchain broadcasts {user_id: user_id, name: website_name}

#TODO: no real way to enforce the way that companies validate 

For now:
app simply returns a challenge and a success message signed with users private key



## TODO:


Type checking with

`from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Book`