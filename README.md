## Ticket Manager

![Flask](https://img.shields.io/badge/Flask-3.0.3-brightgreen.svg)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2.27.0-brightgreen.svg)
A Web Application in Flask that implements a simple ticket system with different user roles and groups

## Installation
1. Clone git repository to your local machine:
```
    https://github.com/OlehOryshchuk/tickets_manager
```
2. Copy the `.env.sample` file to `.env` and configure the environment variables
```
    cp .env.sample .env
```
3. Run command. Docker should be installed:
```
    docker-compose up --build
```
4. Access Web Server as admin you can use the following admin user account:

- **Username** Admin1_
- **Password** afspo982_&(_

### Usage
To access the API, navigate to http://localhost:8000/ in your web browser and enter one of endpoints.

### Endpoints
Tickets Manager endpoints 

user_id - is the book integer id
- `/users/` - returns paginated list of users
- `/users/user_id/` - user detail endpoint
- `/users/me/` - current use profile
- `/users/me/edit` - update your account

Available only to admins:
- `/users/user_id/` - delete, or change user status


gr_id - is the group integer id

Available only to admins:
- `/groups/` - return paginated list of groups
- `/groups/create/` - create group view
- `/admin/groups/gr_id` - group detail view
- `/groups/gr_id` - group delete view
- `/groups/gr_id/update` - update group

Available only to admins, analyst and manager:
- `/groups/gr_id/` - group detail view if you are assigned to that group only

tck_id - is the ticket integer id
Available only to admins, analyst and manager:
- `/tickets/` - list of tickets for admin will show all tickets for rest of roles will show
tickets of the groups they are assigned to.
- `/tickets/tck_id` - detail ticket view admin can view all tickets rest of roles should be assigned to the
group that ticket belongs to
- `/tickets/tck_id` - delete ticket, analyst and manager can delete it if they are assign to the group `ticket_id` belong to.
- `/tickets/tck_id/update` - update ticket view analyst and manager can update it if they are assign to the group `ticket_id` belong to.
