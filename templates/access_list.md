Access           | Groups
---------------- | ---------------------------------------- 
{% for access, groups in summary %}{{ access.strip().ljust(16) }} | {{ groups.strip().ljust(40) }}
{% endfor %}
