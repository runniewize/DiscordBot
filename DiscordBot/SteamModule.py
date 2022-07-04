# from requests_html import HTMLSession

# html_session = HTMLSession()
# steam_response = html_session.get("https://store.steampowered.com/specials#p=0&tab=TopSellers")

# day_offers_tab = steam_response.html.find("body > div.responsive_page_frame > div.responsive_page_content > div.responsive_page_template_content > div.contenthub_page_background > div.page_contenthub_content > div.page_content_ctn > div.page_content > div.rightcol > div.contenthub_dailydeal_container > div.dailydeal_ctn") #TopSellersRows
# first_day_offer = day_offers_tab[0].find("div.discount_block")

# first_sale_value = first_day_offer[0].find("div.discount_pct")[0].text #скидка

# first_day_offer_link = day_offers_tab[0].absolute_links

# first_sale = [first_sale_value, first_day_offer_link] # скидка + ссылка


# second_day_offer = day_offers_tab[1].find("div.discount_block")

# second_sale_value = second_day_offer[0].find("div.discount_pct")[0].text #скидка

# second_day_offer_link = day_offers_tab[1].absolute_links

# second_sale = [second_sale_value, second_day_offer_link]


#print(first_sale)
#print(second_sale)


