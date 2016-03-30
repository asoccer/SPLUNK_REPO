import praw
import sys
#PRAW is a Reddit API Package
def main(argv):
	if(len(argv)<3):
		#Need 3 arguments, USER,PASS, SUBREDDIT
		print("Please enter your USER,PASS,SUBREDDIT for ModLogBot to parse")
		sys.exit(2)
	#Create user agent
	r = praw.Reddit("Modlog to Splunk")	
		
	user = argv[0]
	password = argv[1]
	try:
		r.login(user,password,disable_warning=True)
	except:
		print("Login failed, please check your internet and try again later")
		sys.exit(2)

	subreddit = argv[2]
	#Last has the subreddit ID set to it so that it can continuly request for a new one
	last = 0
	#Output file
	outfile = open("Output_ModLog.txt","w")
	#Count how many actions I want
	counter =0 
	#Request for modaction generator
	Modlog = r.get_mod_log(subreddit,limit=100)
	print("Beginning log run!")
	while(counter<50000):
		
		for log in Modlog:
			log_str = "{},{},{},{},".format(log.mod,log.target_author,str(log),log.created_utc)
			print(log_str,file=outfile)
			counter+=1
			if(counter%5000==0):
				print("%d actions parsed",counter)
		last = log.id
		Modlog = r.get_mod_log(subreddit,limit=100,params={"after":last})
	print("Job is done, now exiting")
	outflie.close()
	sys.exit(2)




#r.login(user,password,disable_warning=True)
#subreddit = 'leagueoflegends'


if __name__== "__main__":
	main(sys.argv[1:])