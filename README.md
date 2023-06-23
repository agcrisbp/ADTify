<h1 align="center">

Spotify APi for [ADLink](https://bit.ly/ADLink-Docs) <br>
<small>(Extends from [spotify-github-profile](https://github.com/kittinan/spotify-github-profile) inspire by [Natemoo-re](https://github.com/natemoo-re))</small>.

</h1>

Create Spotify now playing card on your [ADLink](https://bit.ly/ADLink-Docs) website.

Running on Vercel serverless function, store data in Firebase (store only access_token, refresh_token, token_expired_timestamp)

### Live Version
![Live](https://spotify.aghea.site/api/view.svg?uid=8glrlrg13vyc6hu8tgw6sfvez&cover_image=true&theme=natemoo-re&show_offline=false&background_color=121212&interchange=true&bar_color=ff73ff)

### Example
![Example](/img/natemoo-re.svg)

### Running for development locally
To develop locally, you need:
- A fork of this project as your repository
- A Vercel project connected with the forked repository
- A Firebase project with Cloud Firestore setup
- A Spotify developer account

#### Setting up Vercel
- [Create a new Vercel project by importing](https://vercel.com/new/import?s=https%3A%2F%2Fgithub.com%2Fagcrisbp%2FSpotify-ADLink&hasTrialAvailable=0&showOptionalTeamCreation=false&project-name=Spotify-ADLink&framework=other&totalProjects=1&remainingProjects=1) this repository.

#### Setting up Firebase
- Create [a new Firebase project](https://console.firebase.google.com/u/0/)
- Create a new Cloud Firestore in the project
- Download configuration JSON file from _Project settings_ > _Service accounts_ > _Generate new private key_
- Convert private key content as BASE64
  - You can use Encode/Decode extension in VSCode to do so
  - This key will be used in step explained below

#### Setting up Spotify Dev
- Login to [developer.spotify.com](https://developer.spotify.com/dashboard/applications)
- Create a new project
- Edit settings to add _Redirect URIs_
  - add `http://localhost:3000/api/callback`

#### Running locally

- Install [Vercel command line](https://vercel.com/download) with `npm i -g vercel`
- Create `.env` file at the root of the project and paste your keys in `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, and `FIREBASE`

```sh
BASE_URL='http://localhost:3000/api'
SPOTIFY_CLIENT_ID='____'
SPOTIFY_SECRET_ID='____'
FIREBASE='__BASE64_FIREBASE_JSON_FILE__'
```

![Example](/img/env.png)

- Run `vercel dev`

```sh
$ vercel dev
Vercel CLI 20.1.2 dev (beta) — https://vercel.com/feedback
> Ready! Available at http://localhost:3000
```

- Now try to access http://localhost:3000/api/login