% Odczyt danych z pliku CSV
clc; clear; close all;
fileID = fopen('export (8).csv', 'r');


data = textscan(fileID, '%f', 'Delimiter', ',', 'HeaderLines', 1);
fclose(fileID);

% Rozdzielenie danych na poszczególne kolumny
data = data{1};
num_rows = numel(data) / 5;
data = reshape(data, 5, num_rows)';
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);
freq = data(:, 4);
meas = data(:, 5);

% Konwersja jednostek

% Wykres XYZ z gradientem kolorów
scatter3(x, y, z, 10, meas, 'filled');
alpha 0.5;
colorbar;

% Dodanie etykiet osi
xlabel('X [mm]');
ylabel('Y [mm]');
zlabel('Z [mm]');

% Ustawienie tytułu wykresu
title('Wykres XYZ z gradientem kolorów');

% Wyświetlenie częstotliwości na tytule kolorowej skali
freq_title = sprintf('Freq = %.2f GHz', freq);
colorbar_title_handle = get(colorbar, 'Title');
set(colorbar_title_handle, 'String', freq_title);

% Ustawienie etykiet na osiach kolorowej skali
c = colorbar;
c.Label.String = 'dBm';

% Ustawienie zakresu wartości dla skali kolorów
caxis([min(meas), max(meas)]);

% Ustawienie rozmiaru i przeźroczystości punktów
h = get(gca, 'Children');
set(h, 'SizeData', 100); % rozmiar punktów
set(h, 'MarkerFaceAlpha', 0.15); % przeźroczystość punktów