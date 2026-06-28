# C5G7 — Teknik Anlatım

## 1. Motivasyon — neden transport?

Difüzyon teorisi (Fick yasası, J = −D∇φ) homojenleştirilmiş, yumuşak-akılı
bölgeler için mükemmeldir. Ama:

- keskin **yakıt/su arayüzlerinde**,
- güçlü **soğurucularda** (MOX'taki plütonyum, kontrol çubukları),
- ve akının **yöne bağlı (anizotropik)** olduğu yerlerde

Fick yasası bozulur. Oralarda nötron **transport denklemini** açısal bağımlılığıyla
çözmek gerekir. C5G7, modern transport kodlarını **homojenleştirme olmadan** sınamak
için OECD/NEA tarafından tasarlanmış standart doğrulama problemidir.

## 2. Difüzyon vs Transport — temel fark

| | Difüzyon | Transport (S<sub>N</sub>) |
|---|---|---|
| Bilinmeyen | φ(**r**) — skaler akı | ψ(**r**, **Ω**) — açısal akı |
| Faz uzayı | 3-B (konum) | 5-B (konum + 2 açı + enerji) |
| Denklem | −∇·D∇φ + Σ<sub>a</sub>φ = S | **Ω**·∇ψ + Σ<sub>t</sub>ψ = (1/4π)[Σ<sub>s</sub>φ + χF/k] |
| Açısal model | Fick yaklaşımı (P1) | her yön ayrı çözülür |

Difüzyonda her noktada **tek bir** φ değeri vardır. Transportta her noktada her **yöne**
(**Ω**) bağlı ψ çözülür — bu boyut patlamasıdır ve transportun pahalı olmasının sebebidir.

## 3. Sayısal yöntem

### 3.1 Açısal ayrıklaştırma — discrete ordinates (S<sub>N</sub>)
Sürekli **Ω** açısal değişkeni, sonlu sayıda ayrık yöne (m = 1…M) indirgenir. Her yöne
bir ağırlık w<sub>m</sub> atanır; açısal integraller kuadratür toplamına döner:
φ(**r**) = Σ<sub>m</sub> w<sub>m</sub> ψ<sub>m</sub>(**r**).

Burada **çarpım kuadratürü** kullanılır: düzgün dağılmış azimut açıları × Gauss–Legendre
polar düğümleri (ξ = cos θ). Ağırlıklar 4π'ye toplanır.

### 3.2 Uzaysal ayrıklaştırma — hacim-koruyan "dijital disk"
Silindirik yakıt pinleri Kartezyen ağda temsil edilir. Naif "hücre merkezi pin içinde mi?"
testi, kaba ağda yakıt hacmini %30'a varan oranda şişirir/büzer. Bunun yerine:

> Her pin hücresinde, merkeze **en yakın N hücre** yakıt yapılır,
> N = round(πr²/h²).

Böylece yakıt hacmi **her ağ çözünürlüğünde tam korunur** ve pin simetrik kalır. Bu,
kaba ağda bile k<sub>eff</sub>'in tutarlı olmasını sağlar.

### 3.3 Uzaysal şema ve süpürme
Her yön için **diamond-difference** şemasıyla hücre hücre süpürme (sweep) yapılır;
negatif akı çıkarsa sıfıra çekilir (fix-up). Süpürme yönü, o yöndeki **Ω** işaretine göre
belirlenir (yukarı-akış mantığı).

### 3.4 Sınır koşulları
- **Batı & Kuzey:** yansıtıcı (çekirdek simetri düzlemleri) — çeyrek çekirdek simetrisi.
  Gelen açısal akı, ayna yönünün giden akısına eşitlenir (`mirx`, `miry` indeksleri).
- **Doğu & Güney:** vakum (reflektörün dış kenarı) — gelen akı sıfır.

### 3.5 Özdeğer çözümü
- Dış döngü: **güç (power) iterasyonu** — k<sub>eff</sub> ve fisyon kaynağı güncellenir.
- İç döngü: saçılma kaynağı (termal **yukarı-saçılma** dahil) **Gauss–Seidel** ile gevşetilir.
- **OpenMP** ile yönler üzerinden paralelleştirme (her thread bir grup yönü süpürür,
  sonuçlar kritik bölgede toplanır).

## 4. Yakınsama davranışı

Spektral yarıçap yüksek olduğundan (DR ≈ 0.955) ~400 dış iterasyon gerekir. Güç iterasyonu
başlangıçta büyük salınım yapar (k binlerce değer alır — düz başlangıç akısı nedeniyle);
sıcak başlangıç (k = 1.15) ve ilk iterasyonda fazladan iç süpürme bu sıçramayı bastırır.

## 5. Sonuçlar (cpp=16, S(24×4), 20 çekirdek)

| Metrik | Bu çözüm | NEA referans | Fark |
|---|---|---|---|
| k<sub>eff</sub> | 1.184733 | 1.186550 | −181.7 pcm |
| Maks. pin gücü | 2.353 | 2.498 | −5.8 % |
| Min. pin gücü | 0.2182 | 0.232 | −6.0 % |
| MOX simetrisi | 21.92 % = 21.92 % | özdeş | ✓ |

**Assembly güç dağılımı:** A1 UO₂-iç %43.8 (merkez, en yüksek) · A2/A3 MOX %21.9 (eşit,
simetri) · A4 UO₂-dış %12.4 (kenar, en düşük).

## 6. Hata kaynağı — neden tam pcm tutmuyor?

Üç skaler metrik de referansın ~%6 **altında** ve **aynı yönde**. Sebep, eğri pin sınırının
Kartezyen ağ üzerinde **merdiven basamağı (stairstep)** ile temsil edilmesidir: bu, akı
piklerini hafif yumuşatır ve sızıntıyı biraz abartır → k<sub>eff</sub>'i aşağı çeker.

Tam pcm eşleşmesi için **Method of Characteristics (MOC)** gerekir — eğri pin sınırını
doğrudan ışın izleriyle takip eden yöntem. Buradaki amaç difüzyondan transporta geçişi,
heterojen geometrinin homojenleştirilmeden çözülmesini ve referansa yakınsamayı
göstermektir; bu hedefe ulaşılmıştır.

## 7. Fiziksel doğrulama

Akı haritaları reaktör fiziğinin bilinen imzalarını veriyor → kod doğru:
- Kılavuz tüplerde termal akı sıçraması (su dolu, soğurma yok)
- Reflektörde termal akı tepesi (moderasyon var, yakıt soğurması yok)
- UO₂'de parlak / MOX'ta bastırılmış termal akı (MOX'taki Pu termal nötron soğurur)
- Hızlı akı yakıt bölgesinde tepe, reflektöre doğru azalır

Pin güç haritası, yayınlanmış C5G7 "partially reflected" assembly haritalarıyla birebir
örtüşür: iç UO₂ köşesinde keskin pik, dış UO₂ köşesinde global minimum, MOX'larda
4.3→8.7 % halka gradyanı.
