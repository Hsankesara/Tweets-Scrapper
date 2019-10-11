# Tweets-Scrapper

This script has helped me to scrap more than 30K+ tweets from more that 40 authors. The script is written such that you only have to give it a list of Twitter handles and output csv file path and it'll download all the tweets, process them and save them to a csv file without any hassle. You can checkout the dataset [here](https://github.com/Hsankesara/The-Tweets-of-Wisdom/blob/master/A%20comprehensive%20study%20of%20wisdom.ipynb) on Github and [here](https://www.kaggle.com/hsankesara/the-tweets-of-wisdom) on Kaggle. Also, I have did a comprehensive data analysis which you can find [here](https://www.kaggle.com/hsankesara/a-comprehensive-study-of-wisdom). You can also checkout the jupyter notebook I have used to scrap 30K+ tweets [here](The_Wisdom_Scrapper.ipynb).

## How the script works

The script will download tweets from all the authors whose Twitter handles are written in the _authors.txt_ file in the **newline seperated format**. The script will download direct tweets, retweets and retweets with a comment. In a retweeted tweet, I took all the information (name and handle) of the orignal author and stored it. Furthermore, Every retweet with a comment contains &lt;Q&gt; and &lt;/Q&gt; tags. The author's comment is followed by &lt;Q&gt; tag and then the content of the retweet comes which is followed by &lt;/Q&gt;.

## How to run it

1. First clone the repository

```bash
git clone https://github.com/Hsankesara/Tweets-Scrapper.git
```

2. Then download the requirements

```bash
cd Tweets-Scrapper
pip3 install -r requirements.txt
```

3. Now, create `cred.json` file which is the copy of `cred.json.sample`,

```bash
cp cred.json.sample cred.json
```

4. Get Twitter credentials and write them in `cred.json` file. You can follow [this](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/) to get your access tokens.
   Now update the `cred.json` file with the tokens you've received from Twitter.

5. Write the Twitter handle of the accounts you want to scrap in _authors.txt_ in **newline seperated format**.

6. run the script

```bash
python3 scrap.py authors.txt tweets.csv
```

7. Wait for it! And you'll get all the tweets soon in the csv format.
