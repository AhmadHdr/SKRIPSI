import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os
import ast  # Untuk evaluasi literal yang aman

def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat data: {e}")
        raise

def create_antecedent(universe, label):
    return ctrl.Antecedent(universe, label)

def create_consequent(universe, label='Takaran'):
    return ctrl.Consequent(universe, label)

def create_fuzzy_sets(fuzzy_var, membership_params):
    for var, params in membership_params:
        if len(params) == 3:
            mf = fuzz.trimf(fuzzy_var.universe, params)
        elif len(params) == 4:
            mf = fuzz.trapmf(fuzzy_var.universe, params)
        else:
            raise ValueError(f"Parameter fungsi keanggotaan untuk '{var}' tidak valid")
        fuzzy_var[var] = mf
        # Simpan parameter ke term
        fuzzy_var.terms[var].params = [float(p) for p in params]  
    return fuzzy_var

def define_membership_functions(temperature, ph):
    temperature_membership_params = [
        ('rendah', [14.0, 14.0, 23.0, 25.0]),
        ('normal', [23.0, 25.0, 29.0, 31.0]),
        ('tinggi', [29.0, 31.0, 40.0, 40.0])
    ]
    temperature = create_fuzzy_sets(temperature, temperature_membership_params)

    ph_membership_params = [
        ('asam', [4.0, 4.0, 5.0, 6.5]),
        ('netral', [5.0, 6.5, 7.5, 9.0]),
        ('basa', [7.5, 9.0, 14.0, 14.0])
    ]
    ph = create_fuzzy_sets(ph, ph_membership_params)

    # print("Fungsi keanggotaan untuk temperature dan pH telah diperbarui.")
    return temperature, ph

def define_feed_membership_functions(weight):
    # Menghitung takaran pakan berdasarkan berat lobster

    membership_params = [
        ('sedikit', [3/100*weight, 3/100*weight, 3.5/100*weight, 3.75/100*weight]),
        ('sedang', [3.5/100*weight, 3.75/100*weight, 4.25/100*weight, 4.5/100*weight]),
        ('banyak', [4.25/100*weight, 4.5/100*weight, 5/100*weight, 5/100*weight])
    ]

    num = int(round((5/100*weight - 3/100*weight), 2)*1000)+1
    feed_universe = np.linspace(3/100*weight, 5/100*weight, num)
    feed_amount = create_consequent(feed_universe)

    feed_amount_mf = create_fuzzy_sets(feed_amount, membership_params)
    return feed_amount_mf, membership_params

def define_rules(temperature, ph, feed_amount):
    rules_list = []
    rules_dict = {}

    rule1 = ctrl.Rule(temperature['normal'] & ph['asam'], feed_amount['sedang'], label='Rule 1')
    rule1.terms = {'Temperature': 'normal', 'pH': 'asam'}
    rules_list.append(rule1)
    rules_dict['Rule 1'] = 'sedang'

    rule2 = ctrl.Rule(temperature['normal'] & ph['netral'], feed_amount['banyak'], label='Rule 2')
    rule2.terms = {'Temperature': 'normal', 'pH': 'netral'}
    rules_list.append(rule2)
    rules_dict['Rule 2'] = 'banyak'

    rule3 = ctrl.Rule(temperature['normal'] & ph['basa'], feed_amount['sedang'], label='Rule 3')
    rule3.terms = {'Temperature': 'normal', 'pH': 'basa'}
    rules_list.append(rule3)
    rules_dict['Rule 3'] = 'sedang'

    rule4 = ctrl.Rule(temperature['rendah'] & ph['asam'], feed_amount['sedikit'], label='Rule 4')
    rule4.terms = {'Temperature': 'rendah', 'pH': 'asam'}
    rules_list.append(rule4)
    rules_dict['Rule 4'] = 'sedikit'

    rule5 = ctrl.Rule(temperature['rendah'] & ph['netral'], feed_amount['sedang'], label='Rule 5')
    rule5.terms = {'Temperature': 'rendah', 'pH': 'netral'}
    rules_list.append(rule5)
    rules_dict['Rule 5'] = 'sedang'

    rule6 = ctrl.Rule(temperature['rendah'] & ph['basa'], feed_amount['sedikit'], label='Rule 6')
    rule6.terms = {'Temperature': 'rendah', 'pH': 'basa'}
    rules_list.append(rule6)
    rules_dict['Rule 6'] = 'sedikit'

    rule7 = ctrl.Rule(temperature['tinggi'] & ph['asam'], feed_amount['sedikit'], label='Rule 7')
    rule7.terms = {'Temperature': 'tinggi', 'pH': 'asam'}
    rules_list.append(rule7)
    rules_dict['Rule 7'] = 'sedikit'

    rule8 = ctrl.Rule(temperature['tinggi'] & ph['netral'], feed_amount['sedang'], label='Rule 8')
    rule8.terms = {'Temperature': 'tinggi', 'pH': 'netral'}
    rules_list.append(rule8)
    rules_dict['Rule 8'] = 'sedang'

    rule9 = ctrl.Rule(temperature['tinggi'] & ph['basa'], feed_amount['sedikit'], label='Rule 9')
    rule9.terms = {'Temperature': 'tinggi', 'pH': 'basa'}
    rules_list.append(rule9)
    rules_dict['Rule 9'] = 'sedikit'

    control_system = ctrl.ControlSystem(rules_list)
    simulation = ctrl.ControlSystemSimulation(control_system)

    # print("Aturan fuzzy telah didefinisikan dan sistem kontrol telah dibuat.")
    return simulation, rules_list, rules_dict


def alpha_cut_intervals(universe, mf, alpha):
    # Mencari interval dari universe di mana mf >= alpha
    # Kemudian mengembalikan min dan max dari interval tersebut
    idx = np.where(mf >= alpha)[0]
    if len(idx) == 0:
        return []
    else:
        # Kita asumsikan mungkin ada lebih dari satu interval.
        # Untuk sederhana, kita gabung semua indeks yang berdekatan menjadi interval tunggal.
        intervals = []
        start = idx[0]
        for i in range(1, len(idx)):
            if idx[i] != idx[i-1] + 1:
                # Terputus, interval selesai
                end = idx[i-1]
                intervals.append((universe[start], universe[end]))
                start = idx[i]
        # Interval terakhir
        end = idx[-1]
        intervals.append((universe[start], universe[end]))
        return intervals

def centroid_defuzzification(universe, mf):
    # Defuzzifikasi centroid sederhana untuk seluruh aggregated_mf
    total_moment = np.sum(universe * mf)
    total_area = np.sum(mf)
    if total_area != 0:
        z = total_moment / total_area
    else:
        z = 0
    return float(z)

def process_data(data_sintetis, temperature, ph):
    results = []
    step = 0.001
    jumlah_data = len(data_sintetis['pH'])-1

    for index, row in data_sintetis.iterrows():

        print(f'Proses data ke {index} dari {jumlah_data} data')

        temp_value = row['Temperature']
        ph_value = row['pH']
        weight_value = row['LobsterWeight']

        feed_amount, feed_membership_params = define_feed_membership_functions(weight_value)

        feed_membership_params_dict = {k: [float(vv) for vv in v] for k, v in feed_membership_params}

        simulation, rules_list, rules_dict = define_rules(temperature, ph, feed_amount)

        # Hitung derajat keanggotaan
        temp_memberships = {}
        for label in temperature.terms:
            membership_value = fuzz.interp_membership(temperature.universe, temperature[label].mf, temp_value)
            temp_memberships[label] = round(float(membership_value), 4)
        ph_memberships = {}
        for label in ph.terms:
            membership_value = fuzz.interp_membership(ph.universe, ph[label].mf, ph_value)
            ph_memberships[label] = round(float(membership_value), 4)

        temperature_membership_params = {
            term: [round(float(v), 2) for v in temperature.terms[term].params]
            for term in temperature.terms
        }
        ph_membership_params = {
            term: [round(float(v), 2) for v in ph.terms[term].params]
            for term in ph.terms
        }

        try:
            activated_rules = []
            aggregated_output = np.zeros_like(feed_amount.universe)
            for rule in rules_list:
                temp_term = rule.terms['Temperature']
                ph_term = rule.terms['pH']
                temp_degree = temp_memberships[temp_term]
                ph_degree = ph_memberships[ph_term]
                activation = min(temp_degree, ph_degree)
                if activation > 0:
                    rule_label = rule.label
                    consequent_label = rules_dict[rule_label]
                    output_mf = feed_amount[consequent_label].mf
                    clipped_mf = np.fmin(activation, output_mf)
                    aggregated_output = np.fmax(aggregated_output, clipped_mf)
                    activated_rules.append({
                        'Rule': rule_label,
                        'Activation': activation,
                        'Temp Degree': temp_degree,
                        'PH Degree': ph_degree,
                        'Consequent': consequent_label
                    })

            if not activated_rules:
                print(f"Tidak ada aturan yang teraktivasi untuk data pada {index}.")
                feed = None
                feed_memberships_output = None
                alpha_predikats = None
                a_values_output = None
            else:
                # Defuzzifikasi centroid
                feed = centroid_defuzzification(feed_amount.universe, aggregated_output)

                # Hitung membership feed untuk nilai defuzzifikasi
                feed_memberships_output = {}
                for label in feed_amount.terms:
                    membership_value = fuzz.interp_membership(feed_amount.universe, feed_amount[label].mf, feed)
                    feed_memberships_output[label] = round(float(membership_value), 4)

                # Alpha_Predikats
                alpha_predikats = {r['Rule']: round(float(r['Activation']), 4) for r in activated_rules}

                # a_values: Sesuai contoh, kita ingin a_values berisi alpha cuts.
                # Kita akan membentuk alpha-cut intervals untuk setiap alpha level dari aturan teraktivasi.
                # Jika ada beberapa aturan, kita akan membuat satu list of dict:
                # Setiap dict: {'alpha_level': activation, 'a_values': [min_val, max_val, ...]}.
                # Jika ada beberapa interval, kita bisa simpan semua, tetapi contoh hanya menunjukkan satu pasang interval.
                # Kita lakukan iterasi untuk setiap alpha level unik.

                a_values_output = []
                # Ambil alpha unique dan urutkan descending agar yang terbesar dulu
                unique_alphas = sorted({ar['Activation'] for ar in activated_rules}, reverse=True)
                for alpha in unique_alphas:
                    intervals = alpha_cut_intervals(feed_amount.universe, aggregated_output, alpha)
                    # intervals bisa lebih dari satu, untuk contoh kita ambil semua:
                    # Format output: {'alpha_level': alpha, 'a_values': [x_start, x_end]...}
                    # Kita flatten jika ada multiple intervals
                    interval_values = []
                    for (start_val, end_val) in intervals:
                        interval_values.extend([round(float(start_val), 2), round(float(end_val), 2)])
                    if interval_values:
                        a_values_output.append({
                            'alpha_level': round(float(alpha), 3),
                            'a_values': interval_values
                        })

                feed = round(float(feed), 4)

        except Exception as e:
            print(f"Terjadi kesalahan saat komputasi pada data {index}: {e}")
            feed = None
            feed_memberships_output = None
            activated_rules = []
            aggregated_output = None
            a_values_output = None
            alpha_predikats = None

        temp_memberships = {k: round(float(v), 4) for k, v in temp_memberships.items()}
        ph_memberships = {k: round(float(v), 4) for k, v in ph_memberships.items()}
        feed_memberships_output = {k: round(float(v), 4) for k, v in feed_memberships_output.items()} if feed_memberships_output != None else None
        feed_membership_params_dict = {k: [round(float(vv), 4) for vv in v] for k, v in feed_membership_params_dict.items()}

        results.append({
            'Temperature': round(float(temp_value), 2),
            'pH': round(float(ph_value), 2),
            'LobsterWeight': round(float(weight_value), 2),
            'feed_amount': feed,
            'Temperature_Membership_Params': temperature_membership_params,
            'PH_Membership_Params': ph_membership_params,
            'Temperature_Memberships': temp_memberships,
            'PH_Memberships': ph_memberships,
            'Takaran_Membership_Params': feed_membership_params_dict,
            'Takaran_Memberships': feed_memberships_output,
            'Alpha_Predikats': alpha_predikats,
            'a_values': a_values_output
        })
    
    return pd.DataFrame(results)

def save_results_to_csv(results: pd.DataFrame, output_file_recommendations, output_file_inferensi):

    # Membuat feed_recommendations.csv
    df_feed_recommendations = results[['Temperature', 'pH', 'LobsterWeight', 'feed_amount']]
    df_feed_recommendations.to_csv(output_file_recommendations, index=False, float_format='%.2f')
    # print(f"Rekomendasi pakan telah disimpan ke {output_file_recommendations}.")

    # Membuat inferensi.csv
    df_inferensi = results.drop(columns=['feed_amount'])
    df_inferensi.to_csv(output_file_inferensi, index=False)
    # print(f"Data inferensi telah disimpan ke '{output_file_inferensi}'.")

def main():
    SYNTHETIC_FILE = '../data/data-sintetis/complete_weight_100.csv'
    OUTPUT_FILE_RECOMMENDATIONS = '../data/data-sintetis/feed_recommendations_complete_weight_100.csv'
    OUTPUT_FILE_INFERENSI = '../data/data-sintetis/inferensi_complete_weight_100.csv'

    # Membuat direktori output jika belum ada
    if not os.path.exists('../data/data-sintetis'):
        os.makedirs('../data/data-sintetis')

    data_sintetis = load_data(SYNTHETIC_FILE)

    temperature_universe = np.linspace(14, 40, 26001)
    ph_universe = np.linspace(4, 14, 10001)
    temperature = create_antecedent(temperature_universe, 'Temperature')
    ph = create_antecedent(ph_universe, 'pH')

    temperature, ph = define_membership_functions(temperature, ph)

    results = process_data(data_sintetis, temperature, ph)

    # if results['LobsterWeight'].unique().shape() == 1:
    #     results.drop(columns=['LobsterWeight'], inplace=True)

    # Memanggil fungsi untuk menyimpan hasil
    save_results_to_csv(results, OUTPUT_FILE_RECOMMENDATIONS, OUTPUT_FILE_INFERENSI)

if __name__ == "__main__":
    main()
