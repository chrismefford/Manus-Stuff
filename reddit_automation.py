#!/usr/bin/env python3.11
"""
Multi-Subreddit Reddit Automation
Monitors multiple leadership/management subreddits and generates tailored content
"""

import json
import os
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Subreddit configurations with tone guidance
SUBREDDITS = {
    'Leadership': {
        'url': 'https://www.reddit.com/r/Leadership/.json',
        'tone': 'thought-provoking, challenging conventional wisdom',
        'focus': 'leadership philosophy, team dynamics, empowerment'
    },
    'managers': {
        'url': 'https://www.reddit.com/r/managers/.json',
        'tone': 'practical, actionable advice for day-to-day management',
        'focus': 'team issues, conflict resolution, performance management'
    },
    'AskManagers': {
        'url': 'https://www.reddit.com/r/AskManagers/.json',
        'tone': 'helpful, direct answers to specific questions',
        'focus': 'workplace dynamics, management challenges, specific situations'
    },
    'Work': {
        'url': 'https://www.reddit.com/r/Work/.json',
        'tone': 'broad, relatable insights across industries',
        'focus': 'workplace culture, job issues, work-life balance'
    },
    'Executives': {
        'url': 'https://www.reddit.com/r/Executives/.json',
        'tone': 'strategic, high-level thinking',
        'focus': 'decision-making, organizational strategy, leadership at scale'
    },
    'BadBosses': {
        'url': 'https://www.reddit.com/r/BadBosses/.json',
        'tone': 'empathetic, constructive reframing, avoid being defensive',
        'focus': 'learning from negative examples, positive leadership lessons'
    },
    'antiwork': {
        'url': 'https://www.reddit.com/r/antiwork/.json',
        'tone': 'constructive, systemic insights, validate concerns',
        'focus': 'workplace issues, power dynamics, employee empowerment'
    }
}

# Google Docs IDs
QUESTIONS_DOC_ID = "1CYECMcw8pPu-a7H27ChbKcRWVnV7PQJKy5QHsSvJElw"
COMMENTS_DOC_ID = "1trD4JzyBQtHEKXt0lVWPfayGo89kM182T_HXAupYP3A"

# Book content summary
BOOK_SUMMARY_FILE = "/home/ubuntu/book_summary.md"

def load_book_content():
    """Load book summary"""
    try:
        with open(BOOK_SUMMARY_FILE, 'r') as f:
            return f.read()
    except:
        return "Leadership concepts from 'Leadership Is Overrated'"

def fetch_subreddit_posts(subreddit_name, url, limit=5):
    """Fetch recent posts from a subreddit"""
    import requests
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data['data']['children'][:limit]:
                post_data = post['data']
                posts.append({
                    'title': post_data.get('title', ''),
                    'selftext': post_data.get('selftext', ''),
                    'author': post_data.get('author', ''),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'subreddit': subreddit_name
                })
            
            return posts
        else:
            print(f"   ⚠ Failed to fetch r/{subreddit_name}: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"   ⚠ Error fetching r/{subreddit_name}: {str(e)}")
        return []

def generate_questions(subreddit_name, config, book_content, num_questions=1):
    """Generate thought-provoking questions for a specific subreddit"""
    
    prompt = f"""You are a leadership expert contributing to r/{subreddit_name}.

SUBREDDIT CONTEXT:
- Tone: {config['tone']}
- Focus: {config['focus']}

BOOK INSIGHTS:
{book_content[:1000]}

Generate {num_questions} thought-provoking question(s) to post as new discussions in r/{subreddit_name}.

For each question, provide:
1. A provocative, attention-grabbing title (question format)
2. A detailed post body (150-250 words) that:
   - Provides context and examples
   - Draws on insights from the book (without mentioning it)
   - Invites discussion and different perspectives
   - Matches the subreddit's tone and focus

IMPORTANT: Return ONLY valid JSON, no other text. Format:
[{{"title": "Question title?", "content": "Post body text..."}}]"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a JSON generator. Return only valid JSON arrays, no markdown, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to parse as JSON object first (in case it's wrapped)
        try:
            data = json.loads(content)
            # If it's an object with a questions key, extract that
            if isinstance(data, dict):
                if 'questions' in data:
                    questions = data['questions']
                elif 'data' in data:
                    questions = data['data']
                else:
                    # Try to find the first list value
                    for value in data.values():
                        if isinstance(value, list):
                            questions = value
                            break
                    else:
                        # Single question as object, wrap in list
                        questions = [data]
            else:
                questions = data
        except:
            # Fallback: try to extract JSON from markdown
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            questions = json.loads(content)
        
        return questions if isinstance(questions, list) else [questions]
    except Exception as e:
        print(f"   ⚠ Error generating questions for r/{subreddit_name}: {str(e)}")
        # Return empty list instead of failing
        return []

def generate_responses(posts, config, book_content, num_responses=3):
    """Generate responses to posts from a specific subreddit"""
    
    if not posts:
        return []
    
    # Select posts to respond to
    selected_posts = posts[:num_responses]
    responses = []
    
    for post in selected_posts:
        prompt = f"""You are responding to a post in r/{post['subreddit']}.

SUBREDDIT CONTEXT:
- Tone: {config['tone']}
- Focus: {config['focus']}

POST:
Title: {post['title']}
Content: {post['selftext'][:500]}

BOOK INSIGHTS:
{book_content}

Write a helpful, thoughtful response (150-300 words) that:
- Matches the subreddit's tone
- Provides genuine value and insights
- Draws on concepts from the book (without mentioning it)
- Is conversational and empathetic
- Avoids self-promotion

Return only the response text, no JSON or formatting."""

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            
            responses.append({
                'post': post,
                'response': response_text
            })
            
            print(f"   - Generated response for: {post['title'][:60]}...")
            
        except Exception as e:
            print(f"   ⚠ Error generating response: {str(e)}")
    
    return responses

def format_questions_content(subreddit_name, questions):
    """Format questions for output with clear visual separators"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create distinctive separator for each subreddit
    content = f"\n\n{'█'*80}\n"
    content += f"{'█'*80}\n"
    content += f"SUBREDDIT: r/{subreddit_name}\n"
    content += f"GENERATED: {timestamp}\n"
    content += f"{'█'*80}\n"
    content += f"{'█'*80}\n\n"
    
    for i, q in enumerate(questions, 1):
        content += f"QUESTION {i} — r/{subreddit_name}\n"
        content += f"{'-'*80}\n"
        content += f"TITLE: {q['title']}\n\n"
        content += f"POST BODY:\n{q['content']}\n\n"
    
    return content

def format_responses_content(subreddit_name, responses):
    """Format responses for output with clear visual separators"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create distinctive separator for each subreddit
    content = f"\n\n{'█'*80}\n"
    content += f"{'█'*80}\n"
    content += f"SUBREDDIT: r/{subreddit_name}\n"
    content += f"GENERATED: {timestamp}\n"
    content += f"{'█'*80}\n"
    content += f"{'█'*80}\n\n"
    
    for i, r in enumerate(responses, 1):
        content += f"RESPONSE {i} — r/{subreddit_name}\n"
        content += f"{'-'*80}\n"
        content += f"POST: {r['post']['title']}\n"
        content += f"AUTHOR: u/{r['post']['author']}\n"
        content += f"URL: {r['post']['url']}\n\n"
        content += f"YOUR RESPONSE:\n{r['response']}\n\n"
    
    return content

def main():
    """Main automation function"""
    print("="*80)
    print("MULTI-SUBREDDIT REDDIT AUTOMATION")
    print("="*80)
    print(f"Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load book content
    print("1. Loading book content...")
    book_content = load_book_content()
    print("   ✓ Book content loaded")
    print()
    
    all_questions_content = ""
    all_responses_content = ""
    
    # Process each subreddit
    for subreddit_name, config in SUBREDDITS.items():
        print(f"2. Processing r/{subreddit_name}...")
        
        # Fetch posts
        print(f"   - Fetching posts...")
        posts = fetch_subreddit_posts(subreddit_name, config['url'], limit=5)
        print(f"   ✓ Found {len(posts)} posts")
        
        # Generate 1 question per subreddit
        print(f"   - Generating question...")
        questions = generate_questions(subreddit_name, config, book_content, num_questions=1)
        print(f"   ✓ Generated {len(questions)} question(s)")
        
        # Generate 3 responses per subreddit
        print(f"   - Generating responses...")
        responses = generate_responses(posts, config, book_content, num_responses=3)
        print(f"   ✓ Generated {len(responses)} responses")
        
        # Format content
        if questions:
            all_questions_content += format_questions_content(subreddit_name, questions)
        if responses:
            all_responses_content += format_responses_content(subreddit_name, responses)
        
        print(f"   ✓ r/{subreddit_name} complete")
        print()
    
    # Save to timestamped files
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    questions_file = f"/home/ubuntu/reddit_questions_{timestamp}.txt"
    responses_file = f"/home/ubuntu/reddit_responses_{timestamp}.txt"
    
    print("3. Saving to files...")
    with open(questions_file, 'w') as f:
        f.write(all_questions_content)
    with open(responses_file, 'w') as f:
        f.write(all_responses_content)
    print(f"   ✓ Questions saved to: {questions_file}")
    print(f"   ✓ Responses saved to: {responses_file}")
    print()
    
    # Append to master files
    print("4. Appending to master files...")
    with open("/home/ubuntu/all_questions.txt", 'a') as f:
        f.write(all_questions_content)
    with open("/home/ubuntu/all_responses.txt", 'a') as f:
        f.write(all_responses_content)
    print("   ✓ Appended to master files")
    print()
    
    # Update Google Docs
    print("5. Updating Google Docs...")
    try:
        import subprocess
        result = subprocess.run(
            ['python3.11', '/home/ubuntu/update_and_format_docs.py', questions_file, responses_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("   ✓ Google Docs updated successfully")
        else:
            print(f"   ⚠ Google Docs update failed: {result.stderr}")
    except Exception as e:
        print(f"   ⚠ Could not update Google Docs: {str(e)}")
    
    print("\n" + "="*80)
    print("RUN COMPLETE!")
    print("="*80)
    print(f"\nProcessed {len(SUBREDDITS)} subreddits")
    print(f"Generated ~{len(SUBREDDITS)} questions and ~{len(SUBREDDITS)*3} responses")
    print(f"\nGoogle Docs:")
    print(f"  Questions: https://docs.google.com/document/d/{QUESTIONS_DOC_ID}/edit")
    print(f"  Comments:  https://docs.google.com/document/d/{COMMENTS_DOC_ID}/edit")
    print(f"\nContent has been automatically posted to your Google Docs!")

if __name__ == "__main__":
    main()
