FROM python:3.5.2
MAINTAINER Santiago Christensen <santiagochristensen@gmail.com>

# Install Django
RUN pip install django==1.10.2 pyyaml==3.12 ua-parser==0.7.1 user-agents humanize==0.5.1 \
  git+git://github.com/selwin/django-user_agents.git@44b752611b4e5cf3df8a053f7aac299ac56f591f \
  shortuuid==0.4.3

# Container startup
COPY start.sh /root/start.sh
CMD ["sh", "/root/start.sh"]
