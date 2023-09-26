# majors_links_without_cards  

Stack: Django + Redis + Celery + PostgreSQL.  


This is one of the components of the larger Majors project. On this server, pairs without cards in 2 and 3 actions are calculated and stored in cache. The website then retrieves the data for users.  
The website fetches spot quotes from various exchanges and recalculates and stores the results using the BestChange exchange service.
