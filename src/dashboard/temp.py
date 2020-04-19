def scrape(request):
    #user_p = UserProfile.objects.filter(user=request.user).first()
    user_p, created = UserProfile.objects.get_or_create(user=request.user)
    user_p.last_scrape = datetime.now(timezone.utc)
    user_p.save()

    session =requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    url = 'https://www.theonion.com/'
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    frontpage = soup.find('div', {'class':'sc-1whp23a-1 fUJpuS'})
    articles = frontpage.find_all('article', {'class':'js_post_item sc-1pw4fyi-6 sOaRj'})
    
    print('---------------------------')
    for article in articles:
        try:
            source = article.find('img')['srcset']
            image_source = source[:(source.index(" "))]
            link = article.find_all('a')[-1]['href']
            headline = article.find('h4', {'class':'sc-1qoge05-0 eoIfRA'})


            # except TypeError:
            #     image_source = 'https://i.kinja-img.com/gawker-media/image/upload/c_fill,fl_progressive,g_center,h_900,q_80,w_1600/aeuxnop6w7njmei7auz7.jpg' #'news/static/the-onion-logo.jpg'
            # except ValueError:
            #     image_source = 'https://i.kinja-img.com/gawker-media/image/upload/c_fill,fl_progressive,g_center,h_900,q_80,w_1600/aeuxnop6w7njmei7auz7.jpg' #'news/static/the-onion-logo.jpg'

            # stackoverflow solution

            media_root = 'C:\/Users/footb/Desktop/Coding/dashly/media_root'
            if not image_source.startswith(("data:image", "javascript")) or image_source == 'news/static/the-onion-logo.jpg':
                local_filename = image_source.split('/')[-1].split("?")[0]
                r = session.get(image_source, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)

                current_image_absolute_path = os.path.abspath(local_filename)
                shutil.move(current_image_absolute_path, media_root)

            # end of stackoverflow

            new_story = Story()
            new_story.title = headline.text
            new_story.url = link
            new_story.image = local_filename
            new_story.save()
            
        except TypeError:
            continue
        except Error:
            continue
    return redirect('/home/')  