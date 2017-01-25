

def issue_last_modified(issue, bot_username):
    dates = []
    dates.append(issue.created_at)
    for event in issue.get_events():
        if event.actor.login != bot_username:
            dates.append(event.created_at)
    for comment in issue.get_comments():
        if comment.user.login != bot_username:
            dates.append(comment.created_at)
    return max(dates)

def issue_warnings(issue, bot_username):
    dates = []
    for comment in issue.get_comments():
        if comment.user.login == bot_username:
            dates.append(comment.created_at)
    return dates

def issue_last_warning(issue, bot_username):
    dates = issue_warnings(issue, bot_username)
    if len(dates) > 0:
        return max(dates)
    else:
        return None

def issue_close(issue, config, days_inactive):
    body = config["messages"]["closing"].format(days_inactive=days_inactive)
    issue.create_comment(body)
    issue.edit(state='closed')


def issue_warning(issue, config, days_inactive, deadline):
    body = config["messages"]["warning"].format(days_inactive=days_inactive, deadline=deadline)
    issue.create_comment(body)

