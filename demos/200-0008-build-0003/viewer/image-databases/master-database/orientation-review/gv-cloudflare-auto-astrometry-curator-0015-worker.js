const HTML_B64 = 'PCFkb2N0eXBlIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CjxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCxpbml0aWFsLXNjYWxlPTEsdmlld3BvcnQtZml0PWNvdmVyIj4KPHRpdGxlPkdhbGF4eSBWaWV3ZXIg4oCUIE9uZS1GaWxlIEF1dG8gQXN0cm9tZXRyeSBDdXJhdG9yIDAwMTI8L3RpdGxlPgo8c3R5bGU+Cjpyb290e2NvbG9yLXNjaGVtZTpkYXJrOy0tYmc6IzA2MDkwZTstLXA6IzBmMTUxZjstLWw6IzJhMzU0NTstLXQ6I2VlZjRmZjstLW06IzllYWNjMDstLWc6IzU1ZTM5YTstLXk6I2ZmZDE2NjstLXI6I2ZmNmI2YjstLWI6IzhhYjRmZn0KKntib3gtc2l6aW5nOmJvcmRlci1ib3h9CmJvZHl7bWFyZ2luOjA7YmFja2dyb3VuZDp2YXIoLS1iZyk7Y29sb3I6dmFyKC0tdCk7Zm9udDoxM3B4IHN5c3RlbS11aSwtYXBwbGUtc3lzdGVtLFNlZ29lIFVJLFJvYm90byxBcmlhbH0KYnV0dG9uLGlucHV0LHNlbGVjdHtmb250OmluaGVyaXQ7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1sKTtiYWNrZ3JvdW5kOiMxMTFhMjY7Y29sb3I6dmFyKC0tdCk7Ym9yZGVyLXJhZGl1czo3cHg7cGFkZGluZzo2cHggOHB4fQpidXR0b24ucHJpbWFyeXtiYWNrZ3JvdW5kOiMxODM0NWQ7Ym9yZGVyLWNvbG9yOiMzNTYyYTU7Zm9udC13ZWlnaHQ6OTAwfQpidXR0b24uZ29vZHtiYWNrZ3JvdW5kOiMxNTMzMjI7Ym9yZGVyLWNvbG9yOiMyYjdhNTY7Zm9udC13ZWlnaHQ6OTAwfQpidXR0b24uYmFke2JhY2tncm91bmQ6IzM1MTUxODtib3JkZXItY29sb3I6I2E5NDI0YTtmb250LXdlaWdodDo5MDB9CmJ1dHRvbi5kYW5nZXJ7YmFja2dyb3VuZDojNGExNzFjO2JvcmRlci1jb2xvcjojZDA0ZTU5O2ZvbnQtd2VpZ2h0OjkwMH0KYnV0dG9uOmRpc2FibGVke29wYWNpdHk6LjQ1fQpoZWFkZXJ7cG9zaXRpb246c3RpY2t5O3RvcDowO3otaW5kZXg6MTAwO2JhY2tncm91bmQ6IzA2MDkwZWY1O2JvcmRlci1ib3R0b206MXB4IHNvbGlkIHZhcigtLWwpO3BhZGRpbmc6NnB4fQouYmFye2Rpc3BsYXk6ZmxleDtnYXA6NXB4O2FsaWduLWl0ZW1zOmNlbnRlcjtmbGV4LXdyYXA6d3JhcH0udGl0bGV7Zm9udC13ZWlnaHQ6OTAwfS5waWxse2JvcmRlcjoxcHggc29saWQgdmFyKC0tbCk7Ym9yZGVyLXJhZGl1czo5OTlweDtwYWRkaW5nOjNweCA3cHg7Zm9udC1zaXplOjExcHh9Lm9re2NvbG9yOnZhcigtLWcpfS53YXJue2NvbG9yOnZhcigtLXkpfS5lcnJ7Y29sb3I6dmFyKC0tcil9Cm1haW57bWF4LXdpZHRoOjEyMDBweDttYXJnaW46YXV0bztwYWRkaW5nOjZweH0ucGFuZWx7YmFja2dyb3VuZDp2YXIoLS1wKTtib3JkZXI6MXB4IHNvbGlkIHZhcigtLWwpO2JvcmRlci1yYWRpdXM6OXB4O3BhZGRpbmc6NnB4O21hcmdpbi1ib3R0b206NnB4fQoucmVjb3Jke2Rpc3BsYXk6ZmxleDtnYXA6NnB4O2FsaWduLWl0ZW1zOmNlbnRlcjtmbGV4LXdyYXA6d3JhcH0ubmFtZXtmb250LXNpemU6MTZweDtmb250LXdlaWdodDo5MDA7ZmxleDoxfS5tZXRhe2ZvbnQtc2l6ZToxMHB4O2NvbG9yOnZhcigtLW0pO3dpZHRoOjEwMCV9Ci5jb21wYXJle2Rpc3BsYXk6Z3JpZDtncmlkLXRlbXBsYXRlLWNvbHVtbnM6MWZyIDFmcjtnYXA6N3B4fS52aWV3e2hlaWdodDptaW4oNjJ2aCw1NjBweCk7bWluLWhlaWdodDozMDBweDtiYWNrZ3JvdW5kOiMwMjA0MDc7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1sKTtib3JkZXItcmFkaXVzOjhweDtwb3NpdGlvbjpyZWxhdGl2ZTtvdmVyZmxvdzpoaWRkZW47ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtqdXN0aWZ5LWNvbnRlbnQ6Y2VudGVyfQoudmlldyBpbWd7d2lkdGg6MTAwJTtoZWlnaHQ6MTAwJTtvYmplY3QtZml0OmNvbnRhaW47b2JqZWN0LXBvc2l0aW9uOmNlbnRlcn0ubGFiZWx7cG9zaXRpb246YWJzb2x1dGU7bGVmdDo1cHg7dG9wOjVweDt6LWluZGV4OjIwO2JhY2tncm91bmQ6IzAwMGM7Ym9yZGVyLXJhZGl1czo1cHg7cGFkZGluZzozcHggNXB4O2ZvbnQtc2l6ZToxMHB4O3BvaW50ZXItZXZlbnRzOm5vbmV9CiNhbGFkaW57d2lkdGg6MTAwJTtoZWlnaHQ6MTAwJX0ucmVhZG91dHtmb250LXNpemU6MTBweDtwYWRkaW5nOjRweCAycHggMDt3aGl0ZS1zcGFjZTpub3dyYXA7b3ZlcmZsb3c6YXV0b30KLmNvbnRyb2xze2Rpc3BsYXk6ZmxleDtnYXA6NXB4O2FsaWduLWl0ZW1zOmNlbnRlcjtmbGV4LXdyYXA6d3JhcH0uY29udHJvbHMrLmNvbnRyb2xze21hcmdpbi10b3A6NXB4fS5jb250cm9scyBsYWJlbHtmb250LXNpemU6MTBweDtjb2xvcjp2YXIoLS1tKTtmb250LXdlaWdodDo5MDB9Ci5zdXJ2ZXl7ZmxleDoxO21pbi13aWR0aDoyNTBweH0ua2V5e2ZsZXg6MTttaW4td2lkdGg6MjIwcHh9CiNzb2x2ZXtmb250LXNpemU6MTVweDtwYWRkaW5nOjlweCAxNHB4fS5zb2x2ZWJveHtib3JkZXI6MXB4IHNvbGlkICMzOTUxNmQ7YmFja2dyb3VuZDojMDkxMTFjO2JvcmRlci1yYWRpdXM6OHB4O3BhZGRpbmc6N3B4fQouc3RhdHVze2ZvbnQtd2VpZ2h0OjkwMDtmb250LXNpemU6MTJweH0uc29sdXRpb257ZGlzcGxheTpncmlkO2dyaWQtdGVtcGxhdGUtY29sdW1uczpyZXBlYXQoNCwxZnIpO2dhcDo1cHg7bWFyZ2luLXRvcDo2cHh9LmNlbGx7Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1sKTtib3JkZXItcmFkaXVzOjdweDtwYWRkaW5nOjVweDt0ZXh0LWFsaWduOmNlbnRlcn0uY2VsbCBzbWFsbHtkaXNwbGF5OmJsb2NrO2NvbG9yOnZhcigtLW0pO2ZvbnQtc2l6ZTo5cHh9LmNlbGwgYntmb250LXNpemU6MTJweH0KLmRlY2lzaW9ue2Rpc3BsYXk6ZmxleDtnYXA6N3B4O2ZsZXgtd3JhcDp3cmFwfS5kZWNpc2lvbiBidXR0b257ZmxleDoxO21pbi13aWR0aDoxMjBweDtwYWRkaW5nOjEwcHh9CiNtYXJrZXJze3Bvc2l0aW9uOmFic29sdXRlO2luc2V0OjA7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4OjI1fS5tYXJre3Bvc2l0aW9uOmFic29sdXRlO3dpZHRoOjEycHg7aGVpZ2h0OjEycHg7Ym9yZGVyOjJweCBzb2xpZCAjNTVmZjk5O2JvcmRlci1yYWRpdXM6NTAlO3RyYW5zZm9ybTp0cmFuc2xhdGUoLTUwJSwtNTAlKTtib3gtc2hhZG93OjAgMCA1cHggIzU1ZmY5OX0ubWFyayBzcGFue3Bvc2l0aW9uOmFic29sdXRlO2xlZnQ6OXB4O3RvcDotOHB4O2JhY2tncm91bmQ6IzAwMGM7Zm9udC1zaXplOjhweDtwYWRkaW5nOjFweCAzcHg7d2hpdGUtc3BhY2U6bm93cmFwfQojY29yc0hlbHB7ZGlzcGxheTpub25lO21hcmdpbi10b3A6NnB4O2JvcmRlcjoxcHggc29saWQgIzhhNzEzMDtib3JkZXItcmFkaXVzOjdweDtwYWRkaW5nOjdweDtjb2xvcjojZmZlM2ExfQpAbWVkaWEobWF4LXdpZHRoOjc2MHB4KXsuY29tcGFyZXtncmlkLXRlbXBsYXRlLWNvbHVtbnM6MWZyfS52aWV3e2hlaWdodDptaW4oNTJ2aCw0NzBweCl9LnNvbHV0aW9ue2dyaWQtdGVtcGxhdGUtY29sdW1uczoxZnIgMWZyfX0KPC9zdHlsZT4KPC9oZWFkPgo8Ym9keT4KPGhlYWRlcj4KIDxkaXYgY2xhc3M9ImJhciI+CiAgPHNwYW4gY2xhc3M9InRpdGxlIj5HViBDTE9VREZMQVJFIEFVVE8gQVNUUk9NRVRSWSBDVVJBVE9SIDAwMTU8L3NwYW4+CiAgPHNwYW4gY2xhc3M9InBpbGwiIGlkPSJwcm9ncmVzcyI+MCAvIDA8L3NwYW4+CiAgPHNwYW4gY2xhc3M9InBpbGwiIGlkPSJhbGFkaW5TdGF0ZSI+QUxBRElO4oCmPC9zcGFuPgogIDxzcGFuIGNsYXNzPSJwaWxsIiBpZD0iYXBpU3RhdGUiPkFTVFJPTUVUUlkgQVBJIOKAlCBSRUFEWTwvc3Bhbj4KICA8YnV0dG9uIGlkPSJwcmV2Ij7il4A8L2J1dHRvbj48YnV0dG9uIGlkPSJuZXh0Ij7ilrY8L2J1dHRvbj4KIDwvZGl2Pgo8L2hlYWRlcj4KCjxtYWluPgogPHNlY3Rpb24gY2xhc3M9InBhbmVsIHJlY29yZCI+CiAgPHNwYW4gY2xhc3M9InBpbGwiIGlkPSJjYXRhbG9nIj7igJQ8L3NwYW4+PHNwYW4gY2xhc3M9Im5hbWUiIGlkPSJuYW1lIj5Mb2FkaW5n4oCmPC9zcGFuPjxzcGFuIGNsYXNzPSJwaWxsIiBpZD0icmVjb3JkU3RhdHVzIj5VTlJFU09MVkVEPC9zcGFuPgogIDxkaXYgY2xhc3M9Im1ldGEiIGlkPSJtZXRhIj7igJQ8L2Rpdj4KIDwvc2VjdGlvbj4KCiA8c2VjdGlvbiBjbGFzcz0iY29tcGFyZSI+CiAgPGRpdiBjbGFzcz0icGFuZWwiPgogICA8ZGl2IGNsYXNzPSJ2aWV3Ij48c3BhbiBjbGFzcz0ibGFiZWwiPlNPVVJDRSBJTUFHRSDigJQgRlVMTCBGUkFNRSAvIE5FVkVSIENST1BQRUQ8L3NwYW4+PGltZyBpZD0icHVibGlzaGVkIj48ZGl2IGlkPSJtYXJrZXJzIj48L2Rpdj48L2Rpdj4KICAgPGRpdiBjbGFzcz0icmVhZG91dCIgaWQ9InNvdXJjZVJlYWRvdXQiPlJBIOKAlCB8IERFQyDigJQgfCBGT1Yg4oCUPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0icGFuZWwiPgogICA8ZGl2IGNsYXNzPSJ2aWV3Ij48c3BhbiBjbGFzcz0ibGFiZWwiPkFMQURJTiDigJQgQVVUT01BVElDIFNPTFVUSU9OPC9zcGFuPjxkaXYgaWQ9ImFsYWRpbiI+PC9kaXY+PC9kaXY+CiAgIDxkaXYgY2xhc3M9InJlYWRvdXQiIGlkPSJhbGFkaW5SZWFkb3V0Ij5SQSDigJQgfCBERUMg4oCUIHwgRk9WIOKAlCB8IFJPVCDigJQ8L2Rpdj4KICA8L2Rpdj4KIDwvc2VjdGlvbj4KCiA8c2VjdGlvbiBjbGFzcz0icGFuZWwgc29sdmVib3giPgogIDxkaXYgY2xhc3M9ImNvbnRyb2xzIj4KICAgPGxhYmVsPkFTVFJPTUVUUlkuTkVUIEFQSSBLRVk8L2xhYmVsPgogICA8aW5wdXQgaWQ9ImFwaWtleSIgY2xhc3M9ImtleSIgdHlwZT0icGFzc3dvcmQiIGF1dG9jb21wbGV0ZT0ib2ZmIiBwbGFjZWhvbGRlcj0icGFzdGUgb25jZTsgc2F2ZWQgb25seSBpbiB0aGlzIGJyb3dzZXIiPgogICA8YnV0dG9uIGlkPSJwcm9maWxlIj5HRVQgLyBWSUVXIEtFWTwvYnV0dG9uPgogICA8YnV0dG9uIGlkPSJzb2x2ZSIgY2xhc3M9InByaW1hcnkiPuKYhSBSVU4gQVVUTyBBTElHTjwvYnV0dG9uPgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbnRyb2xzIj48c3BhbiBjbGFzcz0ic3RhdHVzIiBpZD0ic29sdmVTdGF0dXMiPlJFQURZIOKAlCBzZXJ2ZXIgYnJpZGdlIHBsYXRlIHNvbHZlLjwvc3Bhbj48L2Rpdj4KICA8ZGl2IGlkPSJjb3JzSGVscCIgc3R5bGU9ImRpc3BsYXk6YmxvY2siPgpTRVJWRVIgQlJJREdFIOKAlCB0aGlzIHdlYnNpdGUgY2FsbHMgaXRzIG93biAvYXBpIGJhY2tlbmQuIENocm9tZSBuZXZlciBjb250YWN0cyBBc3Ryb21ldHJ5Lm5ldCBkaXJlY3RseS4KVGhlIEFQSSBrZXkgaXMgbm90IHN0b3JlZCBieSB0aGUgYmFja2VuZC4KPC9kaXY+CiAgPGRpdiBjbGFzcz0ic29sdXRpb24iPgogICA8ZGl2IGNsYXNzPSJjZWxsIj48c21hbGw+U09MVkVEIFJBPC9zbWFsbD48YiBpZD0ic3JhIj7igJQ8L2I+PC9kaXY+CiAgIDxkaXYgY2xhc3M9ImNlbGwiPjxzbWFsbD5TT0xWRUQgREVDPC9zbWFsbD48YiBpZD0ic2RlYyI+4oCUPC9iPjwvZGl2PgogICA8ZGl2IGNsYXNzPSJjZWxsIj48c21hbGw+U09MVkVEIEZPVjwvc21hbGw+PGIgaWQ9InNmb3YiPuKAlDwvYj48L2Rpdj4KICAgPGRpdiBjbGFzcz0iY2VsbCI+PHNtYWxsPlNPTFZFRCBST1RBVElPTjwvc21hbGw+PGIgaWQ9InNyb3QiPuKAlDwvYj48L2Rpdj4KICA8L2Rpdj4KIDwvc2VjdGlvbj4KCiA8c2VjdGlvbiBjbGFzcz0icGFuZWwiPgogIDxkaXYgY2xhc3M9ImNvbnRyb2xzIj4KICAgPGxhYmVsPlNVUlZFWTwvbGFiZWw+CiAgIDxzZWxlY3QgaWQ9InN1cnZleSIgY2xhc3M9InN1cnZleSI+PC9zZWxlY3Q+CiAgIDxidXR0b24gaWQ9Im1pc3Npb25EZWZhdWx0Ij5NSVNTSU9OIERFRkFVTFQ8L2J1dHRvbj4KICAgPGJ1dHRvbiBpZD0icmVsb2FkU3VydmV5cyI+QUxMIEFWQUlMQUJMRSBIRVJFPC9idXR0b24+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0ibWV0YSI+Q2hhbmdpbmcgc3VydmV5IGNoYW5nZXMgb25seSB0aGUgd2F2ZWxlbmd0aC9iYWNrZ3JvdW5kLiBJdCBkb2VzIG5vdCBjaGFuZ2UgdGhlIHBsYXRlIHNvbHV0aW9uLjwvZGl2PgogPC9zZWN0aW9uPgoKIDxzZWN0aW9uIGNsYXNzPSJwYW5lbCBkZWNpc2lvbiI+CiAgPGJ1dHRvbiBpZD0ieWVzIiBjbGFzcz0iZ29vZCI+WUVTIOKAlCBBQ0NFUFQgU09MVVRJT048L2J1dHRvbj4KICA8YnV0dG9uIGlkPSJubyIgY2xhc3M9ImJhZCI+Tk8g4oCUIEtFRVAgRk9SIFJFVklFVzwvYnV0dG9uPgogIDxidXR0b24gaWQ9InJlbW92ZSIgY2xhc3M9ImRhbmdlciI+UkVNT1ZFIEdBTEFYWTwvYnV0dG9uPgogPC9zZWN0aW9uPgoKIDxzZWN0aW9uIGNsYXNzPSJwYW5lbCBjb250cm9scyI+CiAgPGxhYmVsPk5PVEUgLyBERUxFVEUgUkVBU09OPC9sYWJlbD48aW5wdXQgaWQ9Im5vdGUiIHN0eWxlPSJmbGV4OjE7bWluLXdpZHRoOjIyMHB4IiBwbGFjZWhvbGRlcj0ib3B0aW9uYWwiPgogIDxidXR0b24gaWQ9ImRvd25sb2FkIj5ET1dOTE9BRCBDVVJBVElPTiBKU09OPC9idXR0b24+CiA8L3NlY3Rpb24+CjwvbWFpbj4KCjxzY3JpcHQ+Cid1c2Ugc3RyaWN0JzsKY29uc3QgQUxBRElOX1VSTD0naHR0cHM6Ly9hbGFkaW4uY2RzLnVuaXN0cmEuZnIvQWxhZGluTGl0ZS9hcGkvdjMvMy44LjIvYWxhZGluLmpzJzsKY29uc3QgTU9DPSdodHRwczovL2FsYXNreWJpcy5jZHMudW5pc3RyYS5mci9Nb2NTZXJ2ZXIvcXVlcnknOwpjb25zdCBDQVRBTE9HUz1bCiB7bmFtZTonQ2hhbmRyYScscmV2OicwMDAyJyx1cmw6J2h0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9nZWFyNjZtZS11aS9HYWxheHlfVmlld2VyL2JldGEvdmlld2VyL2ltYWdlLWRhdGFiYXNlcy9DaGFuZHJhL2RhdGFiYXNlcy9ndi1jaGFuZHJhLWdhbGF4aWVzLWZ1bGwtMDAwMi5qc29uJ30sCiB7bmFtZTonSHViYmxlJyxyZXY6JzAwMjUnLHVybDonaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2dlYXI2Nm1lLXVpL0dhbGF4eV9WaWV3ZXIvYmV0YS92aWV3ZXIvaW1hZ2UtZGF0YWJhc2VzL0h1YmJsZS9kYXRhYmFzZXMvZ3YtaHViYmxlLWdhbGF4aWVzLWZ1bGwtMDAyNS5qc29uJ30sCiB7bmFtZTonSldTVCcscmV2OicwMDAyJyx1cmw6J2h0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9nZWFyNjZtZS11aS9HYWxheHlfVmlld2VyL2JldGEvdmlld2VyL2ltYWdlLWRhdGFiYXNlcy9KV1NUL2RhdGFiYXNlcy9ndi1qd3N0LWdhbGF4aWVzLWZ1bGwtMDAwMi5qc29uJ30sCiB7bmFtZTonU3BpdHplcicscmV2OicwMDA5Jyx1cmw6J2h0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS9nZWFyNjZtZS11aS9HYWxheHlfVmlld2VyL2JldGEvdmlld2VyL2ltYWdlLWRhdGFiYXNlcy9TcGl0emVyL2RhdGFiYXNlcy9ndi1zcGl0emVyLWdhbGF4aWVzLWZ1bGwtMDAwOS5qc29uJ30KXTsKY29uc3QgREVGQVVMVD17CiBIdWJibGU6e2lkOidDRFMvUC9IU1QvY29sb3InLHRpdGxlOidIU1QgQ29sb3InfSwKIEpXU1Q6e2lkOidDRFMvUC9KV1NUL0VQTycsdGl0bGU6J0pXU1QgT3V0cmVhY2ggLyBFUE8nfSwKIENoYW5kcmE6e2lkOidodHRwczovL2NkYWZ0cC5jZmEuaGFydmFyZC5lZHUvUC9jZGEvaGlwcy9hbGxza3kvcmdiJyx0aXRsZTonQ2hhbmRyYSBDREEgWC1yYXkgUkdCJ30sCiBTcGl0emVyOntpZDonQ0RTL1AvU1BJVFpFUi9jb2xvcicsdGl0bGU6J1NwaXR6ZXIgSVJBQyBDb2xvcid9Cn07CmNvbnN0IENST1NTPVsKIHtpZDonUC9EU1MyL2NvbG9yJyx0aXRsZTonRFNTMiBDb2xvciDigJQgb3B0aWNhbCd9LAoge2lkOidDRFMvUC9QYW5TVEFSUlMvRFIxL2NvbG9yLWktci1nJyx0aXRsZTonUGFuLVNUQVJSUyBEUjEgQ29sb3Ig4oCUIChpLHIsZyknfSwKIHtpZDonUC8yTUFTUy9jb2xvcicsdGl0bGU6JzJNQVNTIENvbG9yIOKAlCBuZWFyLUlSJ30sCiB7aWQ6J1AvU0RTUzEvY29sb3InLHRpdGxlOidTRFNTOSBDb2xvciDigJQgb3B0aWNhbCd9Cl07CmNvbnN0IFNUT1JFPScnZ3YtY2xvdWRmbGFyZS1hdXRvLWFzdHJvbWV0cnktY3VyYXRvci0wMDE1JzsKbGV0IHJvd3M9W10saWR4PTAsYWxhZGluPW51bGwscmV2aWV3PXt9LHNvbHV0aW9uPW51bGw7CnRyeXtyZXZpZXc9SlNPTi5wYXJzZShsb2NhbFN0b3JhZ2UuZ2V0SXRlbShTVE9SRSl8fCd7fScpfWNhdGNoe30KY29uc3QgJD1zPT5kb2N1bWVudC5xdWVyeVNlbGVjdG9yKHMpOwoKLy8gMDAxMyBGSVg6IHJlc3RvcmUgdGhlIHNhdmVkIGtleSBvbmx5IEFGVEVSIGAkYCBleGlzdHMuCnRyeXsKICBjb25zdCBzYXZlZEtleT1sb2NhbFN0b3JhZ2UuZ2V0SXRlbSgnZ3YtYXN0cm9tZXRyeS1hcGkta2V5Jyl8fCc nOwogICQoJyNhcGlrZXknKS52YWx1ZT1zYXZlZEtleTsKICAkKCcjYXBpU3RhdGUnKS50ZXh0Q29udGVudD1zYXZlZEtleT8nQlJJREdFIOKAlCBLRVkgU0FWRUQnOidCUklER0Ug4oCUIEtFWSBSRVFVSVJFRCc7CiAgJCgnI2FwaVN0YXRlJyk uY2xhc3NOYW1lPSdwaWxsICcrKHNhdmVkS2V5Pydvayc6J3dhcm4nKTsKfWNhdGNoe30KZnVuY3Rpb24gc2F2ZSgpe2xvY2FsU3RvcmFnZS5zZXRJdGVtKFNUT1JFLEpTT04uc3RyaW5naWZ5KHJldmlldykpfQpmdW5jdGlvbiBlbnRyaWVzKGQpe2lmKEFycmF5LmlzQXJyYXkoZCkpcmV0dXJuIGQ7Zm9yKGNvbnN0IGsgb2YgWydlbnRyaWVzJywnZ2FsYXhpZXMnLCdyZWNvcmRzJywnaXRlbXMnLCdkYXRhJywnY2F0YWxvZyddKWlmKEFycmF5LmlzQXJyYXkoZD8uW2tdKSlyZXR1cm4gZFt rXTtyZXR1cm5bXX0KZnVuY3Rpb24gbWlzc2luZyh2KXtyZXR1cm4gdj09bnVsbHx8KHR5cGVvZiB2PT09J3N0cmluZyc mJiF2LnRyaW0oKSl9CmZ1bmN0aW9uIG5hbWVPZihyKXtyZXR1cm4gci5kaXNwbGF5TmFtZXx8ci5uYW1lfHxyLnRpdGxlfHxyLmRlc2lnbmF0aW9ufHxyLmFyY2hpdmVJZHx8J1VubmFtZWQnfQpmdW5jdGlvbiBuKHYpe2NvbnN0IHg9TnVtYmVyKHYpO3JldHVybiBOdW1iZXIuaXNGaW5pdGUoeCk/eDpudWxsfQpmdW5jdGlvbiByYU9mKHIpe2Zvcihjb25zdCBrIG9mIFsncmEnLCdSQScsJ3JhRGVnJywncmFEZWdyZWVzJ10pe2NvbnN0IHg9bihyW2tdKTtpZih4IT09bnVsbClyZXR1cm4geH1yZXR1cm4gbnVsbH0KZnVuY3Rpb24gZGVjT2Yocil7Zm9yKGNvbnN0IGsgb2YgWydkZWMnLCdEZWMnLCdERUMnLCdkZWNEZWcnLCdkZWNEZWdyZWVzJ10pe2NvbnN0IHg9bihyW2tdKTtpZih4IT09bnVsbClyZXR1cm4geH1yZXR1cm4gbnVsbH0KZnVuY3Rpb24gZm92T2Yocil7bGV0IHY9ci5maWVsZE9mVmlldz8/ci5mb3Y/P3IuRk9WPz9yLmZpZWxkX29mX3ZpZXc7aWYodHlwZW9mIHY9PT0nbnVtYmVyJyYmTnVtYmVyLmlzRmluaXRlKHYpKXJldHVybiB2PjA/djpudWxsO2lmKEFycmF5LmlzQXJyYXkodikpe2NvbnN0IGE9di5tYXAoTnVtYmVyKS5maWx0ZXIoeD0+TnVtYmVyLmlzRmluaXRlKHgpJiZ4PjApO3JldHVybiBhLmxlbmd0aD9NYXRoLm1heCguLi5hKTpudWxsfWNvbnN0IHM9U3RyaW5nKHY/PycnKS50b0xvd2VyQ2FzZSgpLGE9KHMubWF0Y2goL1xkKyg/OlwuXGQrKT8vZyl8fFtdKS5tYXAoTnVtYmVyKTtpZighYS5sZW5ndGgpcmV0dXJuIG51bGw7bGV0IHg9TWF0aC5tYXgoLi4uYSk7aWYoL2FyY3NlY3xhcmNzZWNvbmR88oCzLy50ZXN0KHMpKXgvPTM2MDA7ZWxzZSBpZigvYXJjbWlufGFyY21pbnV0ZXzigLIvLnRlc3QocykpeC89NjA7ZWxzZSBpZighL2RlZ3JlZXxcYmRlZ1xifMKwLy50ZXN0KHMpJiZ4PjIwKXgvPTYwO3JldHVybiB4PjA/eDpudWxsfQpmdW5jdGlvbiBpbWFnZU9mKHIpe3JldHVybiByLnNlbGVjdGVkSW1hZ2VVcmx8fHIuZ2l0aHViSW1hZ2VVcmx8fHIuZXNhUHVibGljYXRpb25KcGVnfHxyLnB1YmxpY2F0aW9uSnBlZ3x8ci5pbWFnZVVybHx8ci5qcGVnVXJsfHxyLmltYWdlfHxBcnJheS5pc0FycmF5KHIuanBlZ0NhbmRpZGF0ZXMpJiZyLmpwZWdDYW5kaWRhdGVzWzBdfHwnJ30KZnVuY3Rpb24gc291cmNlT2Yocil7cmV0dXJuIHIuc291cmNlVXJsfHxyLnNvdXJjZVBhZ2VVcmx8fHIuc291cmNlUGFnZXx8ci5hcmNoaXZlVXJsfHxyLmluZm9Vcmx8fHIud2ViVXJsfHwnJ30KZnVuY3Rpb24ga2V5T2YoYyxyKXtyZXR1cm4gYy5uYW1lKyc6Jysoci5hcmNoaXZlSWR8fHIuaWR8fHIuZGVzaWduYXRpb258fHIubmFtZSl9CmZ1bmN0aW9uIGN1cigpe3JldHVybiByb3dzW2lkeF19CmZ1bmN0aW9uIHNldFN0YXR1cyh0LGNsPSd3YXJuJyl7JCgnI3NvbHZlU3RhdHVzJykudGV4dENvbnRlbnQ9dDskKCcjc29sdmVTdGF0dXMnKS5jbGFzc05hbWU9J3N0YXR1cyAnK2NsfQphc3luYyBmdW5jdGlvbiBsb2FkQWxhZGluKCl7aWYoIXdpbmRvdy5BKXt9fQ==';
const NOVA = 'https://nova.astrometry.net';

function htmlText() {
  const bin = atob(HTML_B64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff'
    }
  });
}

function htmlResponse() {
  return new Response(htmlText(), {
    status: 200,
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff',
      'referrer-policy': 'no-referrer',
      'permissions-policy': 'camera=(), microphone=(), geolocation=()'
    }
  });
}

function finiteNumber(value, name) {
  const n = Number(value);
  if (!Number.isFinite(n)) throw new Error(`${name} must be finite`);
  return n;
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function normalizeRotation(v) {
  v = Number(v) || 0;
  while (v > 180) v -= 360;
  while (v <= -180) v += 360;
  return v;
}

async function novaPost(path, payload) {
  const body = new URLSearchParams();
  body.set('request-json', JSON.stringify(payload));

  const r = await fetch(NOVA + path, {
    method: 'POST',
    headers: {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'},
    body: body.toString(),
    redirect: 'follow'
  });

  const txt = await r.text();
  let j = {};
  try { j = JSON.parse(txt); } catch {}

  if (!r.ok) throw new Error(`Astrometry.net ${path} HTTP ${r.status}`);
  return j;
}

async function novaGet(path) {
  const r = await fetch(NOVA + path, {
    headers: {accept: 'application/json'},
    redirect: 'follow'
  });

  const txt = await r.text();
  let j = {};
  try { j = JSON.parse(txt); } catch {}

  if (!r.ok) throw new Error(`Astrometry.net ${path} HTTP ${r.status}`);
  return j;
}

async function handleSolve(request) {
  if (request.method !== 'POST') return jsonResponse({error: 'POST required'}, 405);

  let b;
  try {
    b = await request.json();
  } catch {
    return jsonResponse({error: 'invalid JSON'}, 400);
  }

  try {
    const apikey = String(b.apikey || '').trim();
    const imageUrl = String(b.image_url || '').trim();

    if (!apikey) throw new Error('Astrometry.net API key is required');
    if (!/^https?:\/\//i.test(imageUrl)) throw new Error('source image must be an http(s) URL');

    const ra = finiteNumber(b.ra, 'ra');
    const dec = finiteNumber(b.dec, 'dec');
    const fov = Math.max(finiteNumber(b.fov, 'fov'), 1e-5);
    const width = Math.max(1, Math.round(finiteNumber(b.width, 'width')));
    const height = Math.max(1, Math.round(finiteNumber(b.height, 'height')));

    const login = await novaPost('/api/login', {apikey});
    if (login.status !== 'success' || !login.session) {
      throw new Error('Astrometry.net login failed');
    }

    const lower = Math.max(fov * 0.25, 0.0005);
    const upper = Math.min(Math.max(fov * 4.0, lower * 2.0), 30.0);
    const radius = clamp(fov * 3.0, 0.25, 15.0);

    const sub = await novaPost('/api/url_upload', {
      session: login.session,
      url: imageUrl,
      allow_commercial_use: 'd',
      allow_modifications: 'd',
      publicly_visible: 'n',
      scale_units: 'degwidth',
      scale_type: 'ul',
      scale_lower: lower,
      scale_upper: upper,
      center_ra: ra,
      center_dec: dec,
      radius,
      downsample_factor: 2,
      crpix_center: true,
      parity: 2
    });

    if (sub.status !== 'success' || !sub.subid) {
      throw new Error('Astrometry.net submission failed: ' + JSON.stringify(sub));
    }

    // Deliberately do not return or persist API key/session.
    return jsonResponse({
      ok: true,
      subid: sub.subid,
      width,
      height,
      search: {
        scale_lower: lower,
        scale_upper: upper,
        radius
      }
    });
  } catch (e) {
    return jsonResponse({error: String(e?.message || e)}, 400);
  }
}

async function handleStatus(url) {
  try {
    const subid = Number(url.searchParams.get('subid'));
    const width = Math.max(1, Number(url.searchParams.get('width')) || 1);
    const height = Math.max(1, Number(url.searchParams.get('height')) || 1);

    if (!Number.isInteger(subid) || subid <= 0) throw new Error('invalid submission id');

    const si = await novaGet('/api/submissions/' + subid);
    const jobs = (si.jobs || []).filter(Boolean);

    if (!jobs.length) {
      if (si.processing_finished) {
        return jsonResponse({
          status: 'error',
          phase: 'FAILED',
          message: 'Astrometry.net finished without a solution'
        });
      }
      return jsonResponse({
        status: 'running',
        phase: 'QUEUE',
        message: `submission ${subid}`
      });
    }

    const jobid = jobs[jobs.length - 1];
    const js = await novaGet('/api/jobs/' + jobid);

    if (js.status === 'failure') {
      return jsonResponse({
        status: 'error',
        phase: 'FAILED',
        message: `Astrometry.net job ${jobid} failed`
      });
    }

    if (js.status !== 'success') {
      return jsonResponse({
        status: 'running',
        phase: 'SOLVING',
        message: `submission ${subid}, job ${jobid}`
      });
    }

    const cal = await novaGet('/api/jobs/' + jobid + '/calibration/');
    let anns = {annotations: []};
    try {
      anns = await novaGet('/api/jobs/' + jobid + '/annotations/');
    } catch {}

    const pix = Number(cal.pixscale);
    if (!Number.isFinite(pix) || pix <= 0) throw new Error('Astrometry.net returned invalid pixel scale');

    const fovx = pix * width / 3600;
    const fovy = pix * height / 3600;
    const solvedFov = Math.max(fovx, fovy);
    const astOrient = Number(cal.orientation) || 0;

    const annotations = (anns.annotations || [])
      .filter(a =>
        a &&
        Array.isArray(a.names) &&
        a.names.length &&
        Number.isFinite(Number(a.pixelx)) &&
        Number.isFinite(Number(a.pixely))
      )
      .slice(0, 7)
      .map(a => ({
        name: String(a.names[0]),
        x: Number(a.pixelx),
        y: Number(a.pixely)
      }));

    return jsonResponse({
      status: 'success',
      phase: 'SOLVED',
      message: `job ${jobid}`,
      result: {
        jobid,
        subid,
        ra: Number(cal.ra),
        dec: Number(cal.dec),
        pixscale_arcsec_per_pixel: pix,
        fov_deg: solvedFov,
        fov_x_deg: fovx,
        fov_y_deg: fovy,
        astrometry_orientation_deg: astOrient,
        aladin_rotation_deg: normalizeRotation(-astOrient),
        parity: Number(cal.parity),
        annotations
      }
    });
  } catch (e) {
    return jsonResponse({error: String(e?.message || e)}, 400);
  }
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'allow': 'GET,POST,OPTIONS',
          'cache-control': 'no-store'
        }
      });
    }

    if (url.pathname === '/api/health') {
      return jsonResponse({
        ok: true,
        service: 'gv-cloudflare-astrometry-bridge-0015'
      });
    }

    if (url.pathname === '/api/solve') {
      return handleSolve(request);
    }

    if (url.pathname === '/api/status') {
      return handleStatus(url);
    }

    if (url.pathname === '/' || url.pathname === '/index.html') {
      return htmlResponse();
    }

    return new Response('Not found', {
      status: 404,
      headers: {'content-type': 'text/plain; charset=utf-8'}
    });
  }
};
