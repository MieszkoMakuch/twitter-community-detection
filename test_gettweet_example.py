import twint

c = twint.Config()
c.Username = "a_humane_being"
c.Custom["tweets"] = ["id", "username"]
c.Output = "tweets.csv"
c.Store_csv = True

# or json
# c.Output = "tweets.json"
# c.Store_json = True

c.Limit = 100

twint.run.Search(c)
