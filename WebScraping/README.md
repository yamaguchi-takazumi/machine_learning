# Webスクレイピングコード

## 実行例

```sh
python3 download_image.py https://exsample.com/image_list.html output
```

## 入力

| 引数      | 型 　    　    |  意味                                  | 備考                    |
| --------- | --------------| -------------------------------------- | ------                 |
| page_url  | str, required | 画像を取得するwebページのURL             |                        |
| outdir    | str, required | 取得画像を保存するディレクトリのパス      | 存在しない場合は新規作成 |
| --keyword | str, option   | `--keyword`がURLに含まれる画像だけを保存 | (default) None         |
| --suffix  | str, option   | 取得画像の拡張子を指定                   | (default) None         |
| --resize  | int, option   | 画像保存時の画像短辺サイズ               | (default) None         |

## 出力

`page_url`の画像が`outdir`に保存される。
但し、

- `--keyword`で指定した文字列をURLに含む画像だけを保存
- `--suffix`で指定した拡張子の画像だけを保存
- 画像保存時に、短辺が`--resize`で指定した値になるよう拡大縮小

## 備考

- `.jpg`と`.png`以外の画像に未対応
- 取得画像は`.jpg`で保存
