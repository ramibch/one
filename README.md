# Django Project Template for my future SaaS sites


## TODO:
- [ ] payments and stripe checkout
- [ ] Plans (Type: TimeFixed, Subscription, NoSubscription, ... )
- [ ] Write units tests
- [ ] admin.py (search, filters...)
- [ ] privacy policy page
- [ ] terms of service page
- [ ] impress
- [ ] match jobs & candidates:
  - [ ] https://github.com/jamesturk/jellyfish/issues/229
  - [ ] https://github.com/seatgeek/thefuzz/issues/90
- [ ] Mail box for users?

## GeoIP2 dbs

(`geoip2dbs`) are stored with GIT LFS.

Here a small description (Credits: Gabriel Staples on stackoverflow):

```bash
# Fetch git lfs files for just the currently-checked-out branch or commit (Ex: 20
# GB of data). This downloads the files into your `.git/lfs` dir but does NOT
# update them in your working file system for the branch or commit you have
# currently checked-out.
git lfs fetch

# Fetch git lfs files for ALL remote branches (Ex: 1000 GB of data), downloading
# all files into your `.git/lfs` directory.
git lfs fetch --all

# Fetch git lfs files for just these 3 branches (Ex: 60 GB of data)
# See `man git-lfs-fetch` for details. The example they give is:
# `git lfs fetch origin main mybranch e445b45c1c9c6282614f201b62778e4c0688b5c8`
git lfs fetch origin main mybranch1 mybranch2

# Check out, or "activate" the git lfs files for your currently-checked-out
# branch or commit, by updating all file placeholders or pointers in your
# active filesystem for the current branch with the actual files these git lfs
# placeholders point to.
git lfs checkout

# Fetch and check out in one step. This one command is the equivalent of these 2
# commands:
#       git lfs fetch
#       git lfs checkout
git lfs pull
#
# Note that `git lfs pull` is similar to how `git pull` is the equivalent
# of these 2 commands:
#       git fetch
#       git merge

```



## Commercial Etsy App

### Requirements

- Please be sure that the application's name follows our Trademark Policy. Application names cannot include “Etsy”, or derivatives of it.
- Within the 'Describe your Application' field, please provide videos or screenshots walking us through your Etsy integration. We're specifically looking to see the functionality of the application, as well as a demonstration of the OAuth authentication process for registering new users.
- We also need to see proof that the notice of attribution has been added to your app or website. The text must read, "The term 'Etsy' is a trademark of Etsy, Inc. This application uses the Etsy API but is not endorsed or certified by Etsy, Inc." Please provide a link to the page on which it’s displayed, or a screenshot of the text within the 'Describe your Application' field.
- https://docs.google.com/forms/d/e/1FAIpQLSfFkfo9drsBoVAA-TYQnBc7evxRHJgNVxkPcrn7AZFF1y4p6w/viewform?pli=1

## Pins

https://help.pinterest.com/en/business/article/pinterest-product-specs



## Source used

- icons: https://icons8.com/icons
