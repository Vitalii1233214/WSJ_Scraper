The server is running on 

    http://154.53.43.187:5005/

In order to perform new scrapping for a current day, please send get request to:

    http://154.53.43.187:5005/scrape_new_urls/

In order to get urls for specific period, the following url should be used:

    http://192.168.1.94:8080/url_between_dates/?start_date={start_date}&end_date={end_date}

example:


    http://154.53.43.187:5005/url_between_dates/?start_date=2022-01-01&end_date=2022-01-03

    
If provided parameters are incorrect, you will see an error message.

Please provide both start and end dates. In case you need urls for a specific day, put start_date=end_date

For scrapping specific url, the following url should be used:

    http://154.53.43.187:5005/scrape_url/?url={url}&username={username}&password={password}

example:

    http://154.53.43.187:5005/scrape_url/?url=https://www.wsj.com/articles/a-european-revelation-on-climate-green-energy-nuclear-natural-gas-france-germany-11641228156&username=avnerroash@gmail.com&password=053960278

if there are some errors during scrapper, you will get the following message: “scrapping error, please check parameters details and try again later”. If you see this error, please try one more time. 

You need to provide url and login details (username and password) to the corresponding parameter field.

IMPORTANT NOTE: Not all articles have the same page format. Moreover, some urls are linked to different web sites (e.g. forex web article). Scrapper doesn’t guarantee the correct collection for such articles from other web resources or when HTML page is built differently. The majority articles have the following format - https://www.wsj.com/articles/a-european-revelation-on-climate-green-energy-nuclear-natural-gas-france-germany-11641228156
Scraper collects all the required data for such article’s format. Any deviations should be treated individually. Since there could be different HTML layouts, we built a scrapper for couple most popular HTML structures. This obstacle increases awaiting time. 

Also, it should be mentioned that scrapping time relates on many factors, such as page loading, internet speed, account time restrictions etc. Not saying that the scrapper process is not fast in general (we need to login and then wait while all information is loaded and then start collecting it). Thus, sometimes it can take up to couple minutes for scrapping a single article. This also might lead to connection time-out during scrapping process. This why we suggest to run link again if the error message appears. 
