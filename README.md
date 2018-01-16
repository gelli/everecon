# everecon
eve.recon - gatecamp checker for eve online

## database
requires fuzzworks postgres sde dump: https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2

Import with: 
```
pg_restore --no-owner -x -h localhost -U<user>  -d<database> postgres-latest.dmp
```
this is a really early prototype!
