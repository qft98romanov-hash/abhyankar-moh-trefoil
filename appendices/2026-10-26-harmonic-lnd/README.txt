ДОПОЛНИТЕЛЬНОЕ ПРИЛОЖЕНИЕ — 26 ОКТЯБРЯ 2026 ГОДА
СТАТУС: НА СТАДИИ ПРОВЕРКИ.
Внешнее независимое рецензирование и литературный приоритет не заявляются.
Все команды запускаются из каталога приложения; некоторые проверки
перезаписывают JSON рядом с собой. История исходных хешей: PROVENANCE.md.
Локальная альтернатива загрузке: python bootstrap_source.py --from-repo ../..
В Windows файлы приложения сохраняются с LF через локальный .gitattributes.
Если исходники в корне рабочего репозитория используют CRLF, офлайн-копия
не совпадёт с Git-хешами: используйте обычный python bootstrap_source.py.
Он получает точные байты зафиксированного коммита; отключать проверки не нужно.

Гармонические вложения, Кремона и LND
Исследовательское продолжение, 26 октября 2026

Начните с harmonic_knots_lnd_research_ru.pdf.
Общая выпрямляемость всех H(a,b,c) здесь НЕ установлена.
Новизна относительно всей литературы отдельно не заявляется.

Подтверждённые результаты:
- Полные семейства H(3,4,c), gcd(c,12)=1, и H(3,5,c), gcd(c,15)=1,
  над Q(sqrt(-3)), посредством двух базовых выпрямлений.
- Явная полиномиальность ядра конкретного LND гипотезы E.
- Минимальные полные степени слайсов: 7 для Shastri и 11 для H(3,5,7).
  Обе нижние границы имеют аналитические доказательства и независимые
  рациональные сертификаты; эти два результата не зависят от репозитория.
- Точный относительный критерий переноса, фильтр исключительных слоёв,
  обструкция конкретного переноса H(3,7,8), нижние границы для параметров.

Источники базовых формул доступны в репозитории:
https://github.com/qft98romanov-hash/abhyankar-moh-trefoil
Фиксированный commit: 3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e
Полная копия исходного репозитория в архив не включена.

ТРЕБОВАНИЯ
Python 3.10+ (проверено 3.12). Для символьных проверок: SymPy 1.14.0.
Не запускать команды с python -O: некоторые исследовательские скрипты
используют стандартные assert. Все расчёты выполняются точно, без float.

БЫСТРЫЕ АВТОНОМНЫЕ ПРОВЕРКИ (только стандартная библиотека Python)
python research/lnd_certificate/verify_minimal_slice.py
python research/repo_audit/review_minimal_slice.py
python research/lnd_certificate/verify_harmonic_minimal_slice.py
python research/repo_audit/review_harmonic_minimal_slice.py

ОСТАЛЬНЫЕ ПРОВЕРКИ
python -m pip install -r requirements.txt
python bootstrap_source.py
python repo/verify.py
python repo/verify_printed_formulas.py
python research/repo_audit/independent_base_lnd.py
python research/harmonic_literature/periodic_shears.py
python research/lnd_certificate/verify_lnd.py
python research/cremona_lnd/verify_example.py
python research/harmonic_compute/verify_new_results.py
python research/harmonic_compute/reduction_scan.py

bootstrap_source.py скачивает только 11 нужных файлов известного коммита
и сверяет размер и Git blob hash с research/source_manifest.json.
Если нет сетевого доступа, можно вручную поместить файлы коммита в repo/.
Скрипт verify_lnd.py принимает путь к исходному verify.py первым аргументом.

Исследовательские parameter_search.py, quadratic_ansatz.py и matrix_probe.py
отделены от сертификатов. Полный поиск базисов Грёбнера может быть дорогим.
Неудача такого поиска не свидетельствует о невыпрямляемости кривой.
Журналы рядом с кодом относятся к выполненным проверкам, не к гипотезам.

СБОРКА PDF
Исходники в latex/. Нужен XeLaTeX с fontspec/polyglossia/unicode-math,
DejaVu Serif, DejaVu Sans и Latin Modern Math.
cd latex
xelatex -interaction=nonstopmode -halt-on-error harmonic_knots_lnd_research_ru.tex
xelatex -interaction=nonstopmode -halt-on-error harmonic_knots_lnd_research_ru.tex

SHA256SUMS.txt содержит хеши итоговых файлов архива.
