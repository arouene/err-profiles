Group            | Users 
---------------- | ---------------------------------------- 
{% for group, users in summary %}{{ group.strip().ljust(16) }} | {{ users.strip().ljust(40) }}
{% endfor %}
