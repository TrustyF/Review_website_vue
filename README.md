
# Trusty's Corner
Welcome! This is my personal media review website / blog. It is published on [trusty-corner.me](https://trusty-corner.me/).

![Screenshot1](https://github.com/TrustyF/Review_website_vue/raw/master/public/home_images/readme_images/readme_screen_2.jpg)

### Dev

* Vue 3
* Python Flask
* Mysql
* Deployed with Firebase.

## Features
### Ratings
Ratings are split into: my personal rating, public rating and the combined circle.

![Screenshot2](https://github.com/TrustyF/Review_website_vue/raw/master/public/home_images/rating_info.jpg)

 The public rating is visually remapped to better match my personal rating distribution.

 The combined circle takes the average of both ratings to provide an easy shorthand of the overall consensus between my personal assessment and the public opinion but also serves as a valuable reference for decision-making. This collaborative approach ensures a more comprehensive and balanced evaluation, taking into account both personal preference and the collective sentiment


### Tags
Medias are annotated with various tags. These are meant to provide a simple breakdown of my opinion, and to help you decide what to pick.

![Screenshot3](https://github.com/TrustyF/Review_website_vue/raw/master/public/home_images/tags_info.jpg)

Tags are categorized into different colors representing their sentiment:

* Gold: the highest honors, the best at what it does
* Green: Positive
* Purple: Caveat or disclaimer
* Red: Negative
* Grey: Gripe or light criticism

### Searchbar
Features a flexible keyword-matching search.

![Screenshot4](https://github.com/TrustyF/Review_website_vue/raw/master/public/home_images/search_info.jpg)

Various Filters can also be applied to match specific attributes like: runtime, release date, rating, etc..
Search fields are matched sequentially:
- name
- genre
- tags
- studio
- author 
Each field attempt to find as much as it can and moves to the next if nothing is returned. This allows for a more intuitive user experience.

### Stats
These are really just to satisfy my own curiosity. Each media category can be graphed if the necessary values are available.

![Screenshot5](https://github.com/TrustyF/Review_website_vue/raw/master/public/home_images/readme_images/readme_screen_3.jpg)

If possible the average personal rating and public rating will be plotted against the specified category.
