SKILLS = ['python', 'java', 'c','c++', 'sql', 'r', 'html', 'json','mysql',
          'css', 'javascript', 'kotlin', 'flutter', 
          
          'numpy', 'pandas', 'pytorch', 'spacy', 'transformers', 
          'faiss', 'scikit-learn', 'sklearn', 'matplotlib', 
          
          'machine learning', 'ml', 'nlp', 'rag', 'embeddings', 
          'data structures', 'database','dbms', 'computer network', 
          'operating system', 'os','data structures and algorithm', 
          'oops', 'dsa', 'oop',
          
          'git', 'github', 'postman','android development', 
          'web development',
          
          'artificial intelligence', 'ai',
          
          'ms word', 'ms excel','powerpoint'
          ]


SKILL_ALIASES={"ml":"machine learning", 
               "machine learning":"machine learning",
               
               "ai":"artificial intelligence",
               "artificial intelligence":"artificial intelligence",
               
               "oop":"oops",
               "oops":"oops",
               
               "sql":"sql",
               "mysql":"sql",
               
               'os':'operating system',
               
               "data structure and algorithm": "data structures and algorithms",
               "data structures and algorithms": "data structures and algorithms"}


SKILL_WEIGHTS={'python':3, 
               'java':3, 
               'c':3,
               'c++':3, 
               'sql':3, 
               'r':3, 
               'html':3, 
               'json':3, 
               'css':3, 
               'javascript':3, 
               'kotlin':3, 
               'flutter':3, 
               'artificial intelligence':3,
               'machine learning':3,
               'data structures and algorithms':3, 
               
               
               'numpy':2,
               'pandas':2, 
               'pytorch':2, 
               'spacy':2, 
               'transformers':2, 
               'faiss':2, 
               'scikit-learn':2, 
               'sklearn':2, 
               'matplotlib':2, 
               'nlp':2, 'rag':2, 
               'embeddings':2, 
               'database':2,
               'git':2, 
               'github':2,
               'oops':2,
               
               'operating system':1,
               'computer network':1, 
               'postman':1,
               'android development':1, 
               'web development':1,
               'ms word':1, 
               'ms excel':1,
               'powerpoint':1}


# skill -> category
SKILL_CATEGORIES = {
    # core
    "python": "core",
    "java": "core",
    "sql": "core",
    "machine learning": "core",
    "data structures and algorithms": "core",
    "artificial intelligence": "core",

    # important
    "pandas": "important",
    "numpy": "important",
    "nlp": "important",
    "git": "important",
    "github": "important",
    "database": "important",
    "dbms": "important",
    "pytorch": "important",
    "transformers": "important",
    "faiss": "important",

    # nice
    "postman": "nice",
    "android development": "nice",
    "web development": "nice",
    "ms word": "nice",
    "ms excel": "nice",
    "powerpoint": "nice",
    "computer network": "nice",
    "operating system": "nice",
}