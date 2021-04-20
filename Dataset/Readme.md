## Dataset Documentation

### Data Sources
* BS Detector (https://www.kaggle.com/mrisdal/fake-news): This data set is based on the "BS detector" browser extension (https://github.com/Bastlynn/bs-detector). This extension uses a manually curated list of misinformational domains to label linked articles as reliable or not. This data set consists of 244 unique domains.

* Columbia Journalism Review (https://www.cjr.org/fake-beta\#methodology): This dataset consists of manually curated misinformational stories scraped from Factcheck (https://www.factcheck.org/2017/07/websites-post-fake-satirical-stories/), Fake News Codex (http://www.fakenewscodex.com/), OpenSources (http://www.opensources.co/), PolitiFact (https://www.politifact.com/) and Snopes (https://www.snopes.com/). This data set consists of 155 unique domains.

* FakeNewsNet (https://github.com/KaiDMML/FakeNewsNet): This data set consists of manually curated misinformational stories scraped from PolitiFact (https://www.politifact.com/) and GossipCop (https://www.gossipcop.com/). This data set consists of 898 unique domains.

* Media Bias Fact Check (https://mediabiasfactcheck.com/fake-news/): This data set consists of a manually curated and continually updated list of news media domains with attributes such as Factual Accuracy, Political Bias, Funding/Ownership, Country, etc. Additionally, this data set contains an evolving list of 100 websites categorized as satire, and 310 websites categorized as conspiracy-pseudoscience. This data set consists of 410 unique domains.

### Cleaning Process
These datasets have several limitations (highlighted in the paper), to contend this we assign each domain i in our original data set a score of ![Tex2Img_1618944211](https://user-images.githubusercontent.com/10993808/115447902-df339780-a1cd-11eb-9b67-94d10978a857.jpg) where r is the Alexa top-million ranking and f is the frequency of the domain in our dataset. Domains with largest score are categorized as misinformational. The file ```raw_data.csv``` consists of individual score of each domain.

### Final 1000 domains (info and misinfo)
Files ```original_1000_fake.csv``` and ```original_1000_real.csv``` contain the misinfo and info domains finally used for the hyperlinks analysis in the paper.
