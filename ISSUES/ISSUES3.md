# ISSUES 3
## Status : Coming Soon

Membuat Option `letx -x [option]` untuk beberapa hal
```
┌──> [ gh0st4n @ T4n-Labs ] <<|= user =|>> [ Thu May 28 ] [ ~ ]
└[T4n OS]->> letx -x pkg discord
=> ERROR: discord-0.0.134_1: does not allow redistribution of sources/binaries (restricted license).
=> ERROR: If you really need this software, run 'echo XBPS_ALLOW_RESTRICTED=yes >> etc/conf'
```

Fix Sementara
```
echo "XBPS_ALLOW_RESTRICTED=yes" | sudo tee -a /usr/lib/python3.14/site-packages/letx/backend/etc/conf
```
