# ChoralCentral

[![Build Status](https://travis-ci.com/chidimo/ChoralCentral.svg?branch=master)](https://travis-ci.com/chidimo/ChoralCentral)
[![Coverage Status](https://coveralls.io/repos/github/chidimo/ChoralCentral/badge.svg?branch=master)](https://coveralls.io/github/chidimo/ChoralCentral?branch=master)

## To do

1. Optimize for search engine and delivery
1. Permissions
1. Management command to clean thumbnails with no score (trigger when score is deleted)
1. Users contribute lyrics and author bio
1. Write tests
1. Suggest names to user based on similarity with already present names. Create it if they're sure its not the same person.
1. Consolidate multiple variation of same author name (Handel, Haendel)
1. Write privacy policy
1. Write terms of use
1. Custom authentication for all API views

## Scenarios in social auth

1. **A clash of emails:** A valid email, `A`, exists as a `primary` account. A social account email, `B`, is now associated with `A`. Someone tries to create a new `primary` account using email `B` that is `secondary` to account `A`. I don't want that.
1. **A clash of providers:** A valid email, `A`, exists as a `primary` account *created non-socially (which means no association was made), but is nonetheless a valid email from provider `X`*. A social account email, `B`, from provider `X` is now associated with `A`. A **non-logged-in** user *invokes* provider `X` with email `A` which already has email `B` secondary to it. Result: `A` is logged-in **AND** a social association is made using provider `X`. Now there are two emails from provider `X` associated with `A`. I don't want that.
