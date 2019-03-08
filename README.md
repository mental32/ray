# ray

![ray_img](ray.webp)

> No longer maintained

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
