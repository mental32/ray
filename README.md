# ray

![ray_img](https://d1u5p3l4wpay3k.cloudfront.net/fortnite_gamepedia/thumb/3/34/Ray.png/250px-Ray.png?version=cd97e8d21d8d45e3c5daff6126b90efb)

A lightweight Fortnite API Library.

```py
import asyncio

import ray

client = ray.Client('username', 'password')

async def main():
    me = await client.get_me()
    friends = await client.get_friends()

    for friend in friends:
        friend_data = await client.get_user_from_id(friend['accountId'])

        for auth in friend_data['externalAuths'].values():
            print(friend['accountId'], '=>', auth['externalDisplayName'])

asyncio.get_event_loop().run_until_complete(main())
```
