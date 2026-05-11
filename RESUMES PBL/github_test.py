from github import Github

# No token needed for public profiles
g = Github()

user = g.get_user("shreyaa008")  

print("Name        :", user.name)
print("Public repos:", user.public_repos)
print("Followers   :", user.followers)
print("Bio         :", user.bio)