from crawler.scraper.crawler import group_articles_by_categories


def test_group_articles_by_category():
    articles_list = [
        dict(author='', category='AMBIENTE', date='', time='',
             title='L’estate 2024 è stata la più calda mai registrata. L’allarme di Copernicus: «Eventi estremi '
                   'sempre più intensi e frequenti»',
             url='https://www.open.online/2024/09/06/estate-2024-piu-calda-mai-registrata-allarme-copernicus-eventi'
                 '-estremi-intensi-frequenti'),
        dict(author='', category='AMBIENTE', date='', time='',
             title='Dall’Italia all’Austria, il pressing dei Paesi Ue per rinviare il regolamento contro la deforestazione',
             url='https://www.open.online/2024/08/29/pressing-paesi-ue-rinvio-regolamento-deforestazione'),
        dict(author='', category='CRONACA', date='', time='',
             title='La storia di Maria, la donna che ha sfidato la mafia e ha vinto: «Ho perso tutto, ma ho salvato la '
                   'mia dignità»',
             url='https://www.open.online/2024/09/06/maria-donna-sfidato-mafia-vinto-perso-tutto-salvato-dignita'),
        dict(author='', category='CRONACA', date='', time='',
             title='La storia di Maria, la donna che ha sfidato la mafia e ha vinto: «Ho perso tutto, ma ho salvato la '
                   'mia dignità»',
             url='https://www.open.online/2024/09/06/maria-donna-sfidato-mafia-vinto-perso-tutto-salvato-dignita'),
        dict(author='', category='CRONACA', date='', time='',
             title='La storia di Maria, la donna che ha sfidato la mafia e ha vinto: «Ho perso tutto, ma ho salvato la '
                   'mia dignità»',
             url='https://www.open.online/2024/09/06/maria-donna-sfidato-mafia-vinto-perso-tutto-salvato-dignita'),
    ]

    articles_by_category = group_articles_by_categories(articles_list)
    assert len(articles_by_category['AMBIENTE']) == 2
    assert len(articles_by_category['CRONACA']) == 3
