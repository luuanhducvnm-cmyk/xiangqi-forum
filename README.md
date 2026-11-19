# xiangqi.forum — site SEO cho Xiangqi 3D & Chess 3D

Site tĩnh (không JavaScript, không framework) gồm **129 trang (tiếng Anh + tiếng Việt)** về cờ tướng (xiangqi) và cờ vua — kèm mục **Tin tức** và **40 bài tập có đáp án** — với **115 sơ đồ bàn cờ** được vẽ từ chính bộ luật của hai game (mọi nước chiếu bí đều được engine kiểm tra lúc build). Mục tiêu: kéo lượt tìm kiếm tự nhiên về
`https://xiangqi3d.online` và `https://chess3d.online` qua nội dung hữu ích, liên kết nội bộ rõ ràng và nút "Chơi ngay" ở các trang liên quan.

> **Nói thẳng:** không ai bảo đảm được "top 1". SEO mất vài tháng để Google tin tưởng một domain mới, và cạnh tranh cho từ khoá như "chinese chess online" rất lớn. Site này đặt nền móng kỹ thuật + nội dung tốt nhất có thể; kết quả phụ thuộc vào thời gian, backlink thật và việc bạn tiếp tục thêm nội dung.

## Cấu trúc

```
build.py            trình dựng site (python3 build.py → dist/)
template.py         HTML/CSS, JSON-LD, breadcrumb, khung trang
content/**/*.md     nội dung (front matter + markdown); content/vi/ = tiếng Việt
tools/specs.py      sơ đồ bàn cờ (FEN + nước đi + expect: mate/stalemate/check)
tools/solver.mjs    bộ giải "chiếu bí trong N nước" dùng ĐÚNG luật của 2 game (key duy nhất, mọi nước đỡ đều bị chiếu bí)
tools/gen-puzzles.mjs, pick.py   sinh ứng viên bài tập ngẫu nhiên → chọn 40 bài đa dạng → tools/puzzles.json
tools/gen_pages.py, puzzle_text.py   giải lại từng bài bằng solver, SINH các trang bài tập vào content/gen/ (cache: puzzle-cache.json)
tools/tablebase.mjs bảng tàn cuộc vét cạn (K+Q/R/P vs K) — căn cứ cho các bài tàn cuộc
tools/lines.mjs, lines.json   dựng thế cờ từ danh sách nước (khai cuộc/bẫy), kiểm từng nước hợp lệ
content/news/, content/vi/tin-tuc/   mục Tin tức (mỗi bài có ngày + nguồn)
content/gen/        trang bài tập do máy sinh — đừng sửa tay
tools/diagrams.py   dựng SVG từ specs (gọi tools/engine.mjs — engine luật của game)
tools/og.py         ảnh chia sẻ 1200×630 + favicon (Playwright) → og-cache/
tools/indexnow.py   báo URL mới/đổi cho Bing/Yandex qua IndexNow
static/             _headers (CSP, cache), file khoá IndexNow
wrangler.toml       triển khai Cloudflare Workers Static Assets
dist/               kết quả build (đừng sửa tay)
```

Mỗi build tự tạo: `sitemap.xml` (có lastmod), `robots.txt`, `feed.xml` (Atom), `llms.txt`, trang `/sitemap/`, `404.html` (noindex), canonical, Open Graph/Twitter card, JSON-LD (Article, BreadcrumbList, FAQPage, SoftwareApplication) và kiểm tra liên kết nội bộ hỏng / sơ đồ không dùng / trang quá mỏng (<250 từ).

## Thêm một trang mới

Tạo `content/<mục>/ten-trang.md`:

```
---
title: Tiêu đề thẻ <title> (≤ ~60 ký tự)
description: Mô tả meta 140–160 ký tự
path: /xiangqi/ten-trang/
section: xiangqi          # xiangqi | chess | news | play | vi | site
order: 7                  # thứ tự trong mục
crumb: Tên ngắn trong breadcrumb
h1: Tiêu đề H1 (tuỳ chọn)
related: /xiangqi/rules/, /xiangqi/openings/
alt: en=/xiangqi/rules/   # chỉ cho trang /vi/: trỏ tới bản tiếng Anh tương ứng (hreflang tự sinh hai chiều)
faq:
- Câu hỏi? | Trả lời ngắn, thật, đúng luật.
---
Nội dung markdown. Dùng {{img:xq-cannon|Chú thích ảnh}} để chèn sơ đồ,
{{cta:xiangqi}} / {{cta:chess}} / {{cta}} để chèn khung "Chơi ngay", {{sitemap}} cho trang sơ đồ.
```

Muốn thêm sơ đồ: thêm một mục vào `tools/specs.py` (FEN, nước đi, `expect`), chạy `python3 build.py`. Nếu "chiếu bí" không đúng luật, build sẽ báo lỗi thay vì xuất sơ đồ sai.

## Build, xem thử, triển khai

```
python3 build.py                 # tạo dist/
python3 tools/og.py              # chỉ khi thêm trang mới (cần Playwright) → ảnh og-cache/
cd dist && python3 -m http.server 8800   # xem thử http://localhost:8800
npx wrangler deploy              # đẩy lên Cloudflare (cần wrangler đăng nhập)
```

### Gắn tên miền xiangqi.forum

1. Thêm domain vào Cloudflare (đổi nameserver về Cloudflare).
2. Trong `wrangler.toml` bỏ comment dòng `routes = [{ pattern = "xiangqi.forum", custom_domain = true }]`, rồi `npx wrangler deploy`.
3. Tạo Redirect Rule trong dashboard: `www.xiangqi.forum` → `https://xiangqi.forum` (301) để chỉ có một phiên bản được lập chỉ mục.

> Site giả định địa chỉ gốc là `https://xiangqi.forum`. Nếu bạn dùng domain khác, đổi hằng `SITE` trong `build.py` và build lại (kể cả liên kết trong `index.html` của 2 game).

## Sau khi lên mạng (bắt buộc, làm trong tuần đầu)

1. **Google Search Console**: thêm property `xiangqi.forum` (xác minh DNS), gửi `https://xiangqi.forum/sitemap.xml`. Làm tương tự cho `xiangqi3d.online` và `chess3d.online` — game cũng đã có `sitemap.xml`, `robots.txt`, canonical, JSON-LD.
2. **Bing Webmaster Tools**: nhập sitemap (có thể import từ Search Console).
3. **IndexNow**: `python3 tools/indexnow.py` sau mỗi lần thêm/sửa trang (file khoá đã có trong `static/`).
4. Dùng "Kiểm tra URL" trong Search Console cho trang chủ và 5–10 trang quan trọng để yêu cầu lập chỉ mục sớm.

## Lộ trình tăng hạng (thực tế)

- **Tháng 0–1:** lên mạng, gửi sitemap, sửa lỗi Search Console báo. Trang chủ game đã trỏ link về các guide, guide trỏ về game (liên kết 2 chiều).
- **Tháng 1–3:** viết thêm 4–8 bài/tháng bám từ khoá dài, ít cạnh tranh: "xiangqi opening for beginners", "how to checkmate with chariot and horse", "xiangqi vs shogi"... Mỗi bài cần ví dụ/sơ đồ riêng, không chép lại bài khác.
- **Tháng 2–6:** backlink thật, không mua: đăng bài hữu ích lên r/xiangqi, r/chess, diễn đàn cờ, Lichess/Chess.com forums (tuân thủ quy định từng nơi, nêu rõ bạn là tác giả), gửi game vào danh sách game trình duyệt/Product Hunt/Hacker News "Show HN", nhờ kênh YouTube/TikTok cờ giới thiệu. Video 9:16 đã làm có thể đăng kèm link guide.
- **Giai đoạn 2:** thêm bài tiếng Anh ngách (đã làm: stalemate, flying general, piece values, kế hoạch học 7 ngày, xiangqi vs shogi; cờ vua: piece values, stalemate, lỗi người mới, kế hoạch 7 ngày, khai cuộc cho người mới). Gợi ý tiếp: perpetual check, "is xiangqi hard", "how to checkmate with king and rook", "chess vs xiangqi", "3D chess online". Bản tiếng Việt đã bật trở lại (xem mục "Khu vực tiếng Việt" và lưu ý pháp lý); bản tiếng Trung chỉ nên cân nhắc sau khi tìm hiểu quy định tương tự của thị trường đích.
- **Tránh:** mua link, bài sinh hàng loạt, nhồi từ khoá, chữ ẩn đánh lừa. Google phạt các thứ này và sẽ làm hỏng cả hai game.

## Đo lường

Search Console (hiển thị, nhấp, vị trí trung bình theo truy vấn/trang), Cloudflare Web Analytics (không cookie, miễn phí), và theo dõi số người vào game từ referrer `xiangqi.forum`. Đánh giá theo xu hướng 4–8 tuần, không theo ngày.

## Cần bạn xác nhận / bổ sung

- **Email liên hệ & thông tin tác giả** cho trang `/about/` (Google ưu tiên nội dung có người chịu trách nhiệm rõ ràng — E-E-A-T). Hiện trang About chỉ nêu thông tin chung.
- Nội dung đang nói game **miễn phí, chơi trên trình duyệt, không cần tải**. Nếu có quảng cáo/bản trả phí, hãy sửa cho khớp.
- Mốc ELO, luật hoà, giới hạn đặt theo **đúng code hiện tại**; nếu đổi luật game, cập nhật `content/play/*.md` và `/elo-rating-explained/`.
- Chưa kiểm thử trên Search Console thật hay trên thiết bị thật: chỉ kiểm tra bằng Chromium giả lập + trình dựng.

## Khu vực tiếng Việt (mặc định vẫn là tiếng Anh)

15 trang tiếng Việt nằm ở `content/vi/` (10 bài cờ tướng + 5 bài cờ vua), có `alt: en=/...` nên mỗi cặp EN↔VI được gắn `hreflang` hai chiều (và `x-default` là bản tiếng Anh) trong HTML lẫn sitemap. Trang tiếng Anh vẫn là mặc định: trang chủ, menu và chân trang tiếng Anh không đổi; chỉ có một liên kết "Tiếng Việt" ở chân trang và liên kết "Đọc bằng tiếng Việt" ở trang có bản dịch. Nút "Chơi" trong trang tiếng Việt mở game bằng `?lang=vi`.

Cả hai game cũng có giao diện tiếng Việt, nhưng **không tự đoán ngôn ngữ** theo trình duyệt/IP: người chơi tự bấm "Tiếng Việt" ở màn hình đầu (game nhớ lựa chọn). Điều khoản/chính sách trong game vẫn tiếng Anh (chưa có bản dịch đã được luật sư rà soát).

> **Lưu ý pháp lý:** vẫn chưa có giấy phép G1 (Nghị định 147/2024/NĐ-CP), nên việc cung cấp giao diện/nội dung tiếng Việt và quảng bá cho người dùng Việt Nam là rủi ro bạn tự quyết định. Bản này không phải tư vấn pháp lý; hãy hỏi luật sư. Muốn tắt: xoá `content/vi/` rồi build lại (và bỏ lựa chọn `vi` trong `i18n.js` của game).


## Chuyển hướng (301)
`static/_redirects` chuyển `/en/play-xiangqi-online/` → `/play/xiangqi-online/` và `/en/play-xiangqi-vs-computer/` → `/play/vs-computer/` (Google Search Console từng báo 2 địa chỉ này là 404/chưa lập chỉ mục vì chúng không có trong site). Triển khai bằng `python3 build.py && npx wrangler deploy` như thường lệ.


## Bài tập và đáp án (đúng do được chứng minh, không gõ tay)

`python3 build.py` tự gọi `tools/gen_pages.py`: mỗi bài trong `tools/puzzles.json` được giải lại bằng `solver.mjs`; build **dừng** nếu bài không có đúng một nước đầu thắng hoặc có cách đỡ không bị chiếu bí. Muốn thêm bài: chạy `node tools/gen-puzzles.mjs xq 2 60 7 > /tmp/c.jsonl` (xq/ch, số nước, số giây, seed), chọn bằng `tools/pick.py`, cập nhật `puzzles.json`.

## Mục Tin tức — cách giữ cho đúng

Mỗi bài trong `content/news/` và `content/vi/tin-tuc/` ghi ngày và danh sách **Nguồn** (FIDE, Chess.com, Wikipedia, báo…). Chỉ ghi điều có trong nguồn đã đọc. Khi có kết quả mới (ví dụ ván đấu vô địch thế giới 24/11–11/12/2026, giải Cờ tướng mở rộng Singapore), hãy sửa/ thêm bài, đổi `updated:` và chạy lại build + `tools/indexnow.py`.

## Tự chứa + tự động deploy (GitHub Actions)

- Repo này **tự chứa**: bộ luật hai game được sao vào `vendor/royal-games/` (solver, sơ đồ, bài tập dùng bản này). Khi sửa luật trong repo game, chép lại 2 file `xiangqi/public/js/rules.js` và `chess/public/js/chess.js` vào `vendor/royal-games/…`.
- `.github/workflows/deploy.yml`: mỗi commit vào nhánh `main` → `python3 build.py` (dừng nếu có lỗi) → `wrangler deploy` → IndexNow. Cần 2 secrets trong GitHub: `CLOUDFLARE_API_TOKEN` (quyền Edit Cloudflare Workers) và `CLOUDFLARE_ACCOUNT_ID`.
- Quy trình khuyến nghị: tác vụ định kỳ đẩy nội dung lên nhánh `draft/<ngày>` và mở Pull Request; bạn đọc rồi bấm Merge = deploy.
- `og-cache/` được commit để CI không cần Playwright; sau khi thêm trang mới hãy chạy `python3 tools/og.py` trên máy có Playwright rồi commit ảnh mới.
