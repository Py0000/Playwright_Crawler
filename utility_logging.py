
def test_check_user_agent(page):
    user_agent = page.evaluate('''() => window.navigator.userAgent''')
    print("User-Agent:", user_agent)

def test_check_referrer(page):
    referrer = page.evaluate('''() => document.referrer''')
    print("Referrer:", referrer)