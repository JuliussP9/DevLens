import os
import sys
import requests
import anthropic
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Set up console for pretty output
console = Console()

# Set up Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_github_data(username):
    headers = {"Accept": "application/vnd.github.v3+json"}

    #Get users profile
    user  = requests.get(
        f"https://api.github.com/users/{username}",
        headers = headers
    ).json()

    #If user is not found
    if "message" in user:
        console.print(f"[red] User '{username}' not found on Github.[/red]")
        sys.exit(1)

    #Get their repos
    repos = requests.get(
        f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated",
        headers = headers
    ).json()

    #How many languages used per repo
    languages = {}
    for repo in repos[:10]:
        language_data = requests.get(repo["languages_url"], headers = headers).json()
        for lang, bytes_written in language_data.items():
            languages[lang] = languages.get(lang, 0) + bytes_written

    return user, repos, languages

def display_languages(languages):
    total = sum(languages.values())
    top = sorted(languages.items(), key = lambda x: x[1], reverse=True)[:5]

    console.print("\n[bold]💻 Top Languages[/bold]")
    for lang, bytes_written in top:
        pct = bytes_written/total
        filled = int(pct*20)
        bar = "█" * filled + "░" * (20 - filled)
        console.print(f"  {lang:<15} {bar} {pct*100:.0f}%")

def analyze_with_claude(user, repos, languages):
    #Build a list of top repos
    top_repos = sorted(repos, key = lambda x: x["stargazers_count"], reverse=True)[:5]
    repo_list = "\n".join([
        f"- {r['name']}: {r['description'] or 'No description'}"
        for r in top_repos
    ])  

    #Top langauges list
    top_langs = sorted(languages.items(), key = lambda x: x[1], reverse=True)[:5]
    lang_list = ", ".join(lang for lang, _ in top_langs) 

    #Claude
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens= 1000,
        messages=[{
            "role": "user",
            "content": f"""Analyze this Github profile and provide:
            1. A 2-3 sentence developer summary
            2. Their top 3 technical strengths
            3. What roles they are best suited for
            4. One interesting observation about their coding style

            GitHub data:
            Name: {user.get('name') or user['login']}
            Bio: {user.get('bio') or 'None'}
            Public repos: {user['public_repos']}
            Followers: {user['followers']}
            Top languages: {lang_list}

            Top repositories:
            {repo_list}

            Be specific and concise."""
                    }]
                )

    return message.content[0].text   

def main():
    # Get username from command line
    if len(sys.argv) < 2:
        console.print("[red]Please provide a GitHub username.[/red]")
        console.print("Usage: python analyzer.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    
    console.print(f"\n[bold green]Analyzing @{username}...[/bold green]\n")
    
    # Fetch all GitHub data
    user, repos, languages = get_github_data(username)
    
    # Display profile panel
    console.print(Panel(
        f"[bold]{user.get('name') or user['login']}[/bold]\n"
        f"{user.get('bio') or ''}\n"
        f"📦 {user['public_repos']} repos  "
        f"👥 {user['followers']} followers  "
        f"📍 {user.get('location') or 'Location not set'}",
        title="👤 GitHub Profile",
        border_style="blue"
    ))
    
    # Display languages
    display_languages(languages)
    
    # Display top repos
    console.print("\n[bold]🚀 Top Repositories[/bold]")
    top_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)[:5]
    for repo in top_repos:
        console.print(
            f"  ⭐ {repo['stargazers_count']}  "
            f"[cyan]{repo['name']}[/cyan] — "
            f"{repo['description'] or 'No description'}"
        )
    
    # Get and display AI analysis
    console.print("\n[bold green]Running AI analysis...[/bold green]")
    analysis = analyze_with_claude(user, repos, languages)
    console.print(Panel(
        analysis,
        title="🧠 AI Analysis",
        border_style="green"
    ))

# Run the program
main()
