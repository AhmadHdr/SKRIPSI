import pandas as pd
import ast
import matplotlib
matplotlib.use('Agg')  # Plot tidak ditampilkan ke layar
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
import os

def create_membership_function(universe, params):
    if len(params) == 4:
        return fuzz.trapmf(universe, params)
    elif len(params) == 3:
        return fuzz.trimf(universe, params)
    else:
        raise ValueError("Parameter fungsi keanggotaan tidak valid: {}".format(params))

def plot_fuzzy_sets(ax, universe, mf_dict, value=None):
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']
    for i, (label, params) in enumerate(mf_dict.items()):
        mf = create_membership_function(universe, params)
        ax.plot(universe, mf, label=label, color=colors[i % len(colors)])
        if value is not None:
            deg = fuzz.interp_membership(universe, mf, value)
            if deg > 0:
                ax.plot(value, deg, 'o', color=colors[i % len(colors)])
    if value is not None:
        ax.axvline(x=value, color='k', linestyle='--')
    ax.legend()
    ax.grid(True)

def highlight_area_under_mf(ax, universe, mf, alpha, color='yellow', alpha_fill=0.4):
    clipped = np.fmin(mf, alpha)
    ax.fill_between(universe, 0, clipped, color=color, alpha=alpha_fill)

def is_on_grid_line(value, grid_step=0.2):
    remainder = (value / grid_step) - round(value / grid_step)
    return abs(remainder) < 1e-9

def label_once(ax, x_val, y_val, text, labeled_positions, eps=0.001, color='red', ha='center', va='top'):
    """
    Hanya menampilkan label jika belum ada label yang posisinya sangat mirip.
    labeled_positions: list of tuples (x,y)
    eps: toleransi untuk menganggap dua titik sama
    """
    for (lx, ly) in labeled_positions:
        if abs(lx - x_val) < eps and abs(ly - y_val) < eps:
            # Sudah ada label di posisi yang hampir sama, jangan print lagi
            return
    # Jika belum ada, tambahkan label
    ax.text(x_val, -0.05, text, ha=ha, va=va, transform=ax.get_xaxis_transform(), color=color)
    # Simpan posisi label
    labeled_positions.append((x_val, y_val))

def label_membership_once(ax, x_val, y_val, text, labeled_positions, eps=0.001, color='green', ha='left', va='bottom'):
    # Untuk label membership di sekitar titik crisp atau lainnya
    for (lx, ly) in labeled_positions:
        if abs(lx - x_val) < eps and abs(ly - y_val) < eps:
            # Sudah ada label di posisi yang hampir sama, jangan print lagi
            return
    # Tampilkan label membership
    ax.text(x_val, y_val, text, ha=ha, va=va, color=color)
    labeled_positions.append((x_val, y_val))

def main():

    inferensi_file = '../data/inferensi.csv'

    df_inferensi = pd.read_csv(inferensi_file)

    # Memilih semua data valid
    df_valid = df_inferensi[(df_inferensi['Temperatur'] != '-') & (df_inferensi['pH'] != '-')]

    # Definisikan rule
    rules_info = {
        'Rule 1': (('normal','asam'), 'sedang'),
        'Rule 2': (('normal','netral'), 'banyak'),
        'Rule 3': (('normal','basa'), 'sedang'),
        'Rule 4': (('rendah','asam'), 'sedikit'),
        'Rule 5': (('rendah','netral'), 'sedang'),
        'Rule 6': (('rendah','basa'), 'sedikit'),
        'Rule 7': (('tinggi','asam'), 'sedikit'),
        'Rule 8': (('tinggi','netral'), 'sedang'),
        'Rule 9': (('tinggi','basa'), 'sedikit'),
    }

    step = 0.001

    for idx, row in df_valid.iterrows():
        time = row['Time']
        safe_time = time.replace(':', '-').replace(' ', '_')
        data_folder = os.path.join('plot-grafik-fuzzy', safe_time)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        try:
            temp_val = float(row['Temperatur']) if row['Temperatur'] != '-' else None
            ph_val = float(row['pH']) if row['pH'] != '-' else None
        except:
            print(f"Data tidak valid pada {time}.")
            continue

        if temp_val is None or ph_val is None:
            print(f"Data pada {time} tidak lengkap.")
            continue

        if (row['Takaran_Membership_Params'] == '-' or 
            row['Temperatur_Membership_Params'] == '-' or 
            row['PH_Membership_Params'] == '-'):
            print(f"Membership params tidak lengkap untuk {time}. Lewati plotting.")
            continue

        temp_mf_params = ast.literal_eval(row['Temperatur_Membership_Params'])
        ph_mf_params = ast.literal_eval(row['PH_Membership_Params'])
        takaran_mf_params = ast.literal_eval(row['Takaran_Membership_Params'])

        if not isinstance(takaran_mf_params, dict) or len(takaran_mf_params) == 0:
            print(f"Takaran membership params kosong atau tidak valid untuk {time}.")
            continue

        if row['Temperatur_Memberships'] == '-' or row['PH_Memberships'] == '-':
            print(f"Memberships tidak lengkap untuk {time}. Lewati.")
            continue
        temp_memberships = ast.literal_eval(row['Temperatur_Memberships'])
        ph_memberships = ast.literal_eval(row['PH_Memberships'])

        alpha_predikats = (ast.literal_eval(row['Alpha_Predikats'])
                           if row['Alpha_Predikats'] != '-' else {})

        a_values = ast.literal_eval(row['a_values']) if row['a_values'] != '-' else []

        temperatur_universe = np.arange(14, 40+step, step)
        ph_universe = np.arange(4, 14+step, step)
        all_takaran_points = [v for vals in takaran_mf_params.values() for v in vals]
        takaran_min = min(all_takaran_points)
        takaran_max = max(all_takaran_points)
        takaran_universe = np.arange(takaran_min, takaran_max+step, step)

        # Plot fungsi keanggotaan tanpa data point
        fig_temp, ax_temp = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_temp, temperatur_universe, temp_mf_params, value=None)
        ax_temp.set_title('Temperatur Membership Functions')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_temperature.png"))
        plt.close(fig_temp)

        fig_ph, ax_ph = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_ph, ph_universe, ph_mf_params, value=None)
        ax_ph.set_title('pH Membership Functions')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_ph.png"))
        plt.close(fig_ph)

        fig_takaran, ax_takaran = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_takaran, takaran_universe, takaran_mf_params, value=None)
        ax_takaran.set_title('Takaran Membership Functions')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_takaran.png"))
        plt.close(fig_takaran)

        # Plot dengan data point
        fig_temp_data, ax_temp_data = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_temp_data, temperatur_universe, temp_mf_params, value=temp_val)
        ax_temp_data.set_title(f'Temperatur (Value={temp_val})')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_temperature_data.png"))
        plt.close(fig_temp_data)

        fig_ph_data, ax_ph_data = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_ph_data, ph_universe, ph_mf_params, value=ph_val)
        ax_ph_data.set_title(f'pH (Value={ph_val})')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_ph_data.png"))
        plt.close(fig_ph_data)

        fig_takaran_data, ax_takaran_data = plt.subplots(figsize=(8,6))
        plot_fuzzy_sets(ax_takaran_data, takaran_universe, takaran_mf_params, value=None)
        ax_takaran_data.set_title('Takaran Membership Functions')
        plt.tight_layout()
        plt.savefig(os.path.join(data_folder, "plot_fuzzy_takaran_data.png"))
        plt.close(fig_takaran_data)

        active_input_combinations = []
        for t_label, t_mu in temp_memberships.items():
            if t_mu > 0:
                for p_label, p_mu in ph_memberships.items():
                    if p_mu > 0:
                        active_input_combinations.append((t_label, p_label, t_mu, p_mu))

        clipped_outputs = []
        for (t_label, p_label, t_mu, p_mu) in active_input_combinations:
            matched_rule = None
            matched_output = None
            for r, ((temp_term, ph_term), takaran_term) in rules_info.items():
                if temp_term == t_label and ph_term == p_label:
                    matched_rule = r
                    matched_output = takaran_term
                    break

            if matched_rule is None:
                continue

            alpha = alpha_predikats.get(matched_rule, min(t_mu, p_mu))
            if alpha == 0:
                alpha = min(t_mu, p_mu)

            fig_infer, ax_infer = plt.subplots(figsize=(8,6))
            colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']
            i = 0
            matched_mf = None
            for lbl, prm in takaran_mf_params.items():
                mf = create_membership_function(takaran_universe, prm)
                ax_infer.plot(takaran_universe, mf, label=lbl, color=colors[i % len(colors)])
                if lbl == matched_output:
                    matched_mf = mf
                i += 1

            if matched_mf is not None:
                ax_infer.axhline(y=alpha, color='red', linestyle='--')
                highlight_area_under_mf(ax_infer, takaran_universe, matched_mf, alpha)
                clipped = np.fmin(matched_mf, alpha)
                clipped_outputs.append(clipped)

            ax_infer.set_title(f"Inferensi untuk {time}\nRule: {matched_rule}\nInput: {t_label}({t_mu:.2f}), {p_label}({p_mu:.2f}) => {matched_output}, alpha={alpha:.2f}")
            ax_infer.set_xlabel('Takaran')
            ax_infer.set_ylabel('Membership Degree')
            ax_infer.grid(True)
            ax_infer.legend()
            ax_infer.set_xlim(takaran_min, takaran_max)
            plt.tight_layout()
            plt.savefig(os.path.join(data_folder, f"plot_inferensi_{matched_rule}.png"))
            plt.close(fig_infer)

        if len(clipped_outputs) > 0:
            aggregated = np.fmax.reduce(clipped_outputs) if len(clipped_outputs) > 1 else clipped_outputs[0]

            # Plot komposisi (dengan garis putus-putus)
            fig_comp, ax_comp = plt.subplots(figsize=(8,6))
            for i, co in enumerate(clipped_outputs):
                ax_comp.plot(takaran_universe, co, linestyle='--', label=f"Rule_Active_{i+1}")
            ax_comp.plot(takaran_universe, aggregated, label='Aggregated', color='black', linewidth=2)
            ax_comp.fill_between(takaran_universe, 0, aggregated, color='yellow', alpha=0.4)

            crisp_value = fuzz.defuzz(takaran_universe, aggregated, 'centroid')
            crisp_membership = fuzz.interp_membership(takaran_universe, aggregated, crisp_value)

            grad = np.gradient(aggregated)
            sign_grad = np.sign(grad)
            change_points = []
            for j in range(1, len(sign_grad)):
                if sign_grad[j] != sign_grad[j-1]:
                    change_points.append(j)

            # List untuk menyimpan posisi yang sudah diberi label
            labeled_positions = []

            # Label change_points
            for cp in change_points:
                x_val = takaran_universe[cp]
                y_val = aggregated[cp]
                ax_comp.plot([x_val, x_val], [0, y_val], linestyle='--', color='red')
                ax_comp.plot(x_val, y_val, 'ro')
                # Label x_val hanya sekali jika belum pernah
                label_once(ax_comp, x_val, y_val, f'{x_val:.2f}', labeled_positions, eps=0.001, color='red')

            # Crisp value line
            # ax_comp.plot([crisp_value, crisp_value], [0, crisp_membership], linestyle=':', color='green')
            # ax_comp.plot(crisp_value, crisp_membership, 'go')

            # Jika crisp_membership bukan grid line, beri label membership
            # if not is_on_grid_line(crisp_membership, 0.2):
                # Label membership pada titik crisp_value
                # Pastikan tidak menumpuk dengan label lain
                # Gunakan koordinat (crisp_value, crisp_membership)
                # Karena ini label membership di dekat titik, koordinat y sama persis sehingga aman
                # Kita gunakan label_membership_once untuk titik membership
                # label_membership_once(ax_comp, crisp_value, crisp_membership, f'{crisp_membership:.4f}', labeled_positions, eps=0.001, color='green')
            # Jika on_grid_line, tidak perlu label

            ax_comp.set_title(f"Hasil Komposisi/Agregasi untuk {time}")
            ax_comp.set_xlabel('Takaran')
            ax_comp.set_ylabel('Membership Degree')
            ax_comp.grid(True)
            ax_comp.legend()
            ax_comp.set_xlim(takaran_min, takaran_max)
            plt.tight_layout()
            plt.savefig(os.path.join(data_folder, "plot_komposisi.png"))
            plt.close(fig_comp)

            # Plot komposisi kedua tanpa garis putus-putus
            fig_comp2, ax_comp2 = plt.subplots(figsize=(8,6))
            ax_comp2.plot(takaran_universe, aggregated, label='Aggregated', color='black', linewidth=2)
            ax_comp2.fill_between(takaran_universe, 0, aggregated, color='yellow', alpha=0.4)
            ax_comp2.set_title(f"Hasil Komposisi/Agregasi untuk {time}")
            ax_comp2.set_xlabel('Takaran')
            ax_comp2.set_ylabel('Membership Degree')
            ax_comp2.grid(True)
            ax_comp2.legend()
            ax_comp2.set_xlim(takaran_min, takaran_max)
            plt.tight_layout()
            plt.savefig(os.path.join(data_folder, "plot_komposisi_no_dashed.png"))
            plt.close(fig_comp2)
        else:
            print(f"Tidak ada rule yang aktif untuk {time}, tidak ada plot komposisi.")

if __name__ == "__main__":
    main()
