import requests
import json
verse='''
The Villain again? Without a doubt
That's his name, don't play it out
Or spray it, when you say it out your mouth
Then gave him a cold shoulder for a hour
And told him take a gold shower, for faking funk, soul power
Stocky, short and cocky
Looked like Apollo Creed after he fought with Rocky
Rhymed in a broken English slang, not cockney
Thirteen, his first queen wore hot knock knees
Had to tell her pops, yo stop cock blocking 'B'
Hold something for your daily 'ya' habit
Then go, bada-bing-bing-bing like ricochet rabbit
How 'bout the sicko say stab it?
There's liquor in the cabinet and a slicker for the crafted
And Heineken, I told him much obliged friend
What I gotta spend, if I only touch her thighs then?
Why his eyes widened
He didn't know your man had a nice surprise hiding
Took pride in riding in a sly wise guy grin
'''

command_json = {
	'verse':verse,
	'topics_weight':1,
	'entities_weight':1,
	'verse_weight':1,
	'query_size':10
}

api_res = requests.get('http://localhost:5000',
	json=command_json)
results = json.loads(api_res.text)
print(results)