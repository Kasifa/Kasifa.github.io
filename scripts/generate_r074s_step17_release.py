#!/usr/bin/env python3
"""Publish the R0.74S analytic package without changing frozen mathematics."""

from __future__ import annotations

import hashlib, html, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.96"
RELEASE = "r074s"
CODE = "R0.74S"
TITLE = "R0.74S｜闭流线复现否定所有次线性绝对时间尾"
FIGURE_ID = "fig-r074s-recurrent-tail-obstruction"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74o.html": "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2",
    PUBLIC / "recap-r0-61-r0-74o.pdf": "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076",
}


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def write_text(target: Path, value: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def write_json(target: Path, value: object) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected recap drift: {target.relative_to(ROOT)}")


def verify_sources() -> None:
    expected = {
        "research/r074s_one_sided_ball_clock_no_gain.md": "178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af",
        "research/r074s_one_sided_ball_clock_certificate.json": "1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219",
        "research/r074s_one_sided_ball_clock_primary_audit.md": "83093d667b0f0ac0af919651c4dd45f87e60b8d2ebde59017f8abdfbd33041b9",
        "research/r074s_one_sided_ball_clock_independent_audit.md": "5ee63f78699891801151171f7fa68e103e52b04d2cc07b20ce48c1d3dd31b209",
        "research/r074s_cross_channel_recombination_no_gain.md": "c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03",
        "scripts/r074s_cross_channel_recombination_certificate.py": "88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c",
        "scripts/r074s_cross_channel_recombination_certificate_independent.rb": "cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef",
        "research/r074s_cross_channel_recombination_certificate.json": "5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63",
        "research/r074s_cross_channel_recombination_certificate_report.md": "548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189",
        "research/r074s_dissipation_rayleigh_gate.md": "e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3",
        "research/r074s_dissipation_rayleigh_primary_audit.md": "304bc2b87b9eb97d4f46d8bc4a77da3b1f11e2c37e95e20956504bb4681b2175",
        "research/r074s_dissipation_rayleigh_independent_audit.md": "efc30eb21e8d4e125d4b189455d4419bca9b5d1f1effeb265edba1cdf4a48233",
        "scripts/r074s_dissipation_rayleigh_certificate.py": "61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a",
        "scripts/r074s_dissipation_rayleigh_certificate_independent.rb": "a4ce5bb0d3f20f549e70b7196487fd9540a5ff7be658d4cd52573d65f1a77ff3",
        "research/r074s_dissipation_rayleigh_certificate.json": "4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1",
        "research/r074s_dissipation_rayleigh_certificate_report.md": "5c566f53e378c9f3fba2a690c3962051142ac00990c1177548b9ae3e956b14cb",
        "research/r074s_defect_relaxed_total_rayleigh_excess.md": "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
        "research/r074s_defect_relaxed_total_rayleigh_primary_audit.md": "dbcba5ea68899faf74e4d38c232c58fdd3a71f1b2dcefb1eb007fcf102cd4f73",
        "research/r074s_defect_relaxed_total_rayleigh_independent_audit.md": "d7cb626b07b735b6ef19c8ca20fff670795e32768f3224a756901b230183d875",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py": "18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb": "b18b0a0b9937b106c5879a9e28996dd6892ab53f19decb7bca4db38c70a11343",
        "research/r074s_defect_relaxed_total_rayleigh_certificate.json": "3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c",
        "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md": "3a6d1e263daa7041edc4083a76c38af44f4fbcd7d2efc8f57592eecbd19ec55a",
        "research/r074s_best_n_last_exit_equivalence.md": "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd",
        "research/r074s_best_n_last_exit_primary_audit.md": "0d326d0b77e499c36aa10fac64db66d4c40e6f0599640df65c915ca8de5f58d1",
        "research/r074s_best_n_last_exit_independent_audit.md": "e67b0f6cfcfa15f8e0b7f4f96670e10a843aabd753dd25d7ce5684e6c993a634",
        "scripts/r074s_best_n_last_exit_certificate.py": "0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65",
        "scripts/r074s_best_n_last_exit_certificate_independent.rb": "d9c0674b79bc532c10366d317ccb10550f0bfd2a825127e87a4ef24633d3ae66",
        "research/r074s_best_n_last_exit_certificate.json": "26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0",
        "research/r074s_best_n_last_exit_certificate_report.md": "1108b72113d84b90ebc5570c2c7b4bfaa1ccdc299525c557979b564109ab6481",
        "research/r074s_paid_branch_last_exit_residual.md": "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
        "research/r074s_paid_branch_last_exit_primary_audit.md": "cf7bbfcb01a5389878a2a9f65ffa0e083863f8f6478986bc10110cfd24e6446c",
        "research/r074s_paid_branch_last_exit_independent_audit.md": "cb33dd2a1fed8a58f285bdb3e7a053480c40b06a899d1a1bd3a18549b6b8125a",
        "scripts/r074s_paid_branch_last_exit_certificate.py": "2763b3fa575ce723a400b6c7e5654d0a64c8a9db470d79097dc5a77769a365a9",
        "research/r074s_paid_branch_last_exit_certificate.json": "8f37a8ce4d6513406297e6ce1e676ceaafa39776723bba839074120f206314de",
        "research/r074s_paid_branch_last_exit_certificate_report.md": "6e25a07a417f96907e5e17da6b561830b75aa1a44d0b4b13fa56107dc31e4a5f",
        "scripts/r074s_paid_branch_last_exit_certificate_independent.rb": "15b77560f41aa22d00447821be501ab5d3c992afa1001063c3ce986f2e9938c9",
        "research/r074s_shared_budget_terminal_trace_obstruction.md": "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693",
        "research/r074s_shared_budget_terminal_trace_primary_audit.md": "d8bf38f4337af366cd450a50622f7105b8925db37cd87c09ce839fe129a058d5",
        "research/r074s_shared_budget_terminal_trace_independent_audit.md": "cfabe4b389c31b7ddeab755f51db8cf7daa88875add33621b0722b4487520f65",
        "scripts/r074s_shared_budget_terminal_trace_certificate.py": "a397d27943fca4d4a487038b5c14956667c7d36b3be5eb069262d2593f8ad2de",
        "research/r074s_shared_budget_terminal_trace_certificate.json": "ea5c9f13ba412703995b2875a26c84fa20779457399ffa9117871b65fafaf8d0",
        "research/r074s_shared_budget_terminal_trace_certificate_report.md": "6e86813ab2b001a8f357af42d952a9104ba70859b32441148ad5cd3ab283ffc4",
        "scripts/r074s_shared_budget_terminal_trace_certificate_independent.rb": "b8309f6bf23d0c75b09c39814e1452e6890a8de712f2974ffbda003a53d7a154",
        "research/r074s_terminal_window_morrey_packing.md": "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f",
        "research/r074s_terminal_window_morrey_primary_audit.md": "77397f923a20cb51382031bc4a8da82944190d4273aca8c316864e053e4c9396",
        "research/r074s_terminal_window_morrey_independent_audit.md": "148a75ca1ed9fdba3d8e0df3d1681f0e3fa4997df76960498faf64ffab9b9c95",
        "scripts/r074s_terminal_window_morrey_certificate.py": "90529ecfd080d3554fc45b63f5734a86f8736834cd6a65365c03fc82fb927a5a",
        "research/r074s_terminal_window_morrey_certificate.json": "741cb443b35a447df112d8078b79150eb21d5de308c4835219e0aa54f5e5b9d6",
        "research/r074s_terminal_window_morrey_certificate_report.md": "e9d5ebee782751b2cad17a4b7a78829ee7c4da6b6d7b828a9d5bb8faadba36ad",
        "scripts/r074s_terminal_window_morrey_certificate_independent.rb": "9c34db7d87b7074febdf5cad4cf437c28be6747017002d45479b024b5a815741",
        "research/r074s_temporal_integrability_morrey_certificate.json": "095e8a7a0ba378ff2178a166cbed81e1f132be055d37165c945020a26466e330",
        "research/r074s_temporal_integrability_morrey_certificate_report.md": "c464af1617391beda5b077e13066629203d408519ab32ee89b2115475346fe2b",
        "research/r074s_temporal_integrability_morrey_independent_audit.md": "332bf2a5b4503b9456bc76b1067bc44cb2d788e37fa7f2e34f10211a700e7ce3",
        "research/r074s_temporal_integrability_morrey_primary_audit.md": "5910f46c0dd401d3766343d75ae3e68bdecb9d8416615fd8feb74d0f560adefd",
        "research/r074s_temporal_integrability_morrey_threshold.md": "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
        "scripts/r074s_temporal_integrability_morrey_certificate.py": "eb313260c16431c1379d1b77a508b8bb7740ac713c014126c08e44bc2d0cfafb",
        "scripts/r074s_temporal_integrability_morrey_certificate_independent.rb": "520d52deb1ba56fb46f841e0856bd8eb14ec5dd4961c90dd3b9ec240f88c9720",
        "research/r074s_outer_collar_corona_obstruction.md": "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9",
        "research/r074s_outer_collar_corona_certificate.json": "1714426abc2bbe0a6f98ea5bced5c15843a68fbe66ed02adef670ee681f42be3",
        "research/r074s_outer_collar_corona_certificate_report.md": "d3a5213ed8a646ccf6b26947a31ad18276c3e6e823c4296e8b1b760deabd05ef",
        "research/r074s_outer_collar_corona_primary_audit.md": "7f7dd6a7bb1ca6e598b4156388037fe6db7c191a7baacd46d9abe43b12c37e90",
        "research/r074s_outer_collar_corona_independent_audit.md": "9baa160a706c962f3eb6911d55882c3bc2f883ccdea6c674689930ab4b4e4156",
        "scripts/r074s_outer_collar_corona_certificate.py": "041328286841e79e8863aca9c5ca9ef7c6ebbab328505c030dd1789c76d03e05",
        "scripts/r074s_outer_collar_corona_certificate_independent.rb": "f7e420a03445a8089cd53e31eed55f00def576d2f76e091bf3aa5c405915ee10",
        "research/r074s_hybrid_flux_tail_equivalence.md": "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d",
        "research/r074s_terminal_crown_coercivity.md": "c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80",
        "research/r074s_hybrid_crown_primary_audit.md": "4b5a9943d69da7d97cd5214f36fed98f09a7f58cada2139e8ab76e6e07d1ce28",
        "research/r074s_hybrid_crown_independent_audit.md": "805707ea3890bd825f1a63cc10985bc24fd5f297c784d1e8b0a1d1c15ba5fef6",
        "research/r074s_hybrid_crown_certificate_report.md": "6777bc9cbfdaf0d079407e24269822e52bb36ffda13b828bdd7440a554050d87",
        "research/r074s_hybrid_crown_certificate.json": "38e4d15c76b4bb9a2523173c0da816d6862f9e24fe59595d9953a7aa9516a7b8",
        "scripts/r074s_hybrid_crown_certificate.py": "84c1d8aac5399b71a98cefc4a8ff6a0e13835c8a19e47bd5693ac76fe2bcced4",
        "scripts/r074s_hybrid_crown_certificate_independent.rb": "e21f186f65052335a2ad97f1fd3dfdeada0d548c9369b7040adb77436320af0e",
        "research/r074s_moving_frame_taylor_vortex_obstruction.md": "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
        "research/r074s_moving_frame_taylor_vortex_primary_audit.md": "1140e3f72ddf9565bb6e9c565aaf10de75c8f04b9417ad12e4cddffbabc9a262",
        "research/r074s_moving_frame_taylor_vortex_independent_audit.md": "30af657d18b428fa0355a8cd93a3cf7b7af452588561259ae53a9a734dc55da2",
        "research/r074s_moving_frame_taylor_vortex_certificate.json": "27f93a7e23268be2c337eef6ae0488a8fb60508c51f6dbf12080807e5f636271",
        "research/r074s_moving_frame_taylor_vortex_certificate_report.md": "9b2868d2e9a7cf0bd574ab347d266da1e30a1426c22d48a20f3a472557eab362",
        "scripts/r074s_moving_frame_taylor_vortex_certificate.py": "ec11a53bfc6221344eabd8b809c72deb8996adb56a2da81a6502bc7b914bb54a",
        "scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb": "9b1fcd3805e162bf7d8f24a2ed0818722dc9413ca709696380d0f02614892677",
        "research/r074s_recurrent_streamline_temporal_tail_obstruction.md": "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5",
        "research/r074s_recurrent_streamline_primary_audit.md": "1efc7a520570c22952d7b06b0486865a767981f5303f102380eb9963754a1d4c",
        "research/r074s_recurrent_streamline_independent_audit.md": "255eea01cea10367b1d4051ea960214112ca8473a8b6df47ead4e199727afff3",
        "research/r074s_recurrent_streamline_literature_audit.md": "6c7c58da5250263e2509aa7c66f66bd7b02ef9fc7b920ce5c409661879a73ec8",
        "research/r074s_recurrent_streamline_certificate.json": "a4acf1769e9b56f372b15bfa0155755cb9f0a55a9a314f431d3df0add6f99c0c",
        "research/r074s_recurrent_streamline_certificate_report.md": "efb25a4068957b17910fdf9c345ad92f383d5525c316cad98d763e642c44d202",
        "research/r074s_recurrent_streamline_independent_report.md": "c3b33e4289ecb69f7958174569b55321cfec029fa1fd004c0fde996296742dc8",
        "scripts/r074s_recurrent_streamline_certificate.py": "139a5ce3d36d11b9480f246cc8f7c5297dd3ca86edb5938849e04b7f9f2eddab",
        "scripts/r074s_recurrent_streamline_independent.rb": "6c5181f64d6db424fa280a1a0886005049863a1eef602202631895ab0b95fadb",
    }
    for relative, expected_hash in expected.items():
        if sha256(ROOT / relative) != expected_hash:
            raise RuntimeError(f"frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074s_one_sided_ball_clock_certificate.json").read_text(encoding="utf-8"))
    if certificate["summary"] != {"exact_passed": 5, "exact_total": 5, "finite_passed": 7, "finite_total": 7, "negative_passed": 4, "negative_total": 4, "result": "PASS", "structural_passed": 55, "structural_total": 55}:
        raise RuntimeError("R0.74S certificate boundary drift")
    step6 = json.loads((ROOT / "research/r074s_cross_channel_recombination_certificate.json").read_text(encoding="utf-8"))
    if step6["summary"] != {"exact_passed": 4, "exact_total": 4, "finite_passed": 8, "finite_total": 8, "structural_passed": 58, "structural_total": 58, "negative_passed": 10, "negative_total": 10, "result": "PASS"}:
        raise RuntimeError("R0.74S Step 6 certificate boundary drift")
    step7 = json.loads((ROOT / "research/r074s_dissipation_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step7["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 8, "finite_total": 8, "negative_mutations_passed": 9, "negative_mutations_total": 9, "structural_passed": 52, "structural_total": 52}:
        raise RuntimeError("R0.74S Step 7 certificate boundary drift")
    step8 = json.loads((ROOT / "research/r074s_defect_relaxed_total_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step8["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 19, "finite_total": 19, "negative_mutations_passed": 20, "negative_mutations_total": 20, "structural_passed": 75, "structural_total": 75}:
        raise RuntimeError("R0.74S Step 8 final certificate boundary drift")
    step9 = json.loads((ROOT / "research/r074s_best_n_last_exit_certificate.json").read_text(encoding="utf-8"))
    if step9["summary"] != {"exact_passed": 9, "exact_total": 9, "finite_passed": 8, "finite_total": 8, "structural_passed": 57, "structural_total": 57, "negative_mutations_passed": 18, "negative_mutations_total": 18}:
        raise RuntimeError("R0.74S Step 9 certificate boundary drift")
    step10 = json.loads((ROOT / "research/r074s_paid_branch_last_exit_certificate.json").read_text(encoding="utf-8"))
    if step10["summary"] != {"exact_total": 12, "exact_passed": 12, "finite_total": 10, "finite_passed": 10, "structural_total": 79, "structural_passed": 79, "negative_mutations_total": 47, "negative_mutations_passed": 47}:
        raise RuntimeError("R0.74S Step 10 certificate boundary drift")
    step11 = json.loads((ROOT / "research/r074s_shared_budget_terminal_trace_certificate.json").read_text(encoding="utf-8"))
    if step11["summary"] != {"all_pass": True, "exact_passed": 14, "exact_total": 14, "finite_passed": 7, "finite_total": 7, "negative_passed": 7, "negative_total": 7, "structural_passed": 34, "structural_total": 34}:
        raise RuntimeError("R0.74S Step 11 certificate boundary drift")
    step12 = json.loads((ROOT / "research/r074s_terminal_window_morrey_certificate.json").read_text(encoding="utf-8"))
    if step12["summary"] != {"all_pass": True, "exact_passed": 16, "exact_total": 16, "finite_passed": 12, "finite_total": 12, "negative_passed": 11, "negative_total": 11, "structural_passed": 51, "structural_total": 51}:
        raise RuntimeError("R0.74S Step 12 certificate boundary drift")
    step13 = json.loads((ROOT / "research/r074s_temporal_integrability_morrey_certificate.json").read_text(encoding="utf-8"))
    if step13["overall_pass"] is not True or step13["summary"] != {"dependency_passed": 4, "dependency_total": 4, "exact_passed": 31, "exact_total": 31, "finite_passed": 11, "finite_total": 11, "negative_passed": 32, "negative_total": 32, "structural_passed": 22, "structural_total": 22}:
        raise RuntimeError("R0.74S Step 13 certificate boundary drift")
    step14 = json.loads((ROOT / "research/r074s_outer_collar_corona_certificate.json").read_text(encoding="utf-8"))
    if step14["overall_pass"] is not True or step14["summary"] != {"dependency_passed": 3, "dependency_total": 3, "exact_passed": 12, "exact_total": 12, "finite_cases": 74287, "finite_passed": 9, "finite_total": 9, "negative_passed": 49, "negative_total": 49, "structural_passed": 37, "structural_total": 37}:
        raise RuntimeError("R0.74S Step 14 certificate boundary drift")
    step15 = json.loads((ROOT / "research/r074s_hybrid_crown_certificate.json").read_text(encoding="utf-8"))
    if step15["overall_pass"] is not True or step15["summary"] != {"dependency_passed": 5, "dependency_total": 5, "finite_cases": 3941, "finite_passed": 9, "finite_total": 9, "negative_passed": 20, "negative_total": 20, "structural_passed": 45, "structural_total": 45}:
        raise RuntimeError("R0.74S Step 15 certificate boundary drift")
    step16 = json.loads((ROOT / "research/r074s_moving_frame_taylor_vortex_certificate.json").read_text(encoding="utf-8"))
    if step16.get("verdict") != "PASS":
        raise RuntimeError("R0.74S Step 16 certificate verdict drift")
    if [row["id"] for row in step16["finite_checks"]] != [
        "taylor_exact_fourier_identities", "abc_independent_exact_screen",
        "N_plus_one_deletion_pigeonhole", "finite_small_R_support_screen",
        "temporal_and_payment_exponents", "terminal_characteristic_screen",
        "complete_payment_and_L1_amplitude_bookkeeping",
    ]:
        raise RuntimeError("R0.74S Step 16 finite inventory drift")
    if sum(row["cases"] for row in step16["finite_checks"]) != 2207:
        raise RuntimeError("R0.74S Step 16 finite case count drift")
    if len(step16["structural_checks"]) != 7 or not all(row["pass"] for row in step16["structural_checks"]):
        raise RuntimeError("R0.74S Step 16 structural boundary drift")
    if len(step16["dependency_checks"]) != 3 or not all(row["pass"] for row in step16["dependency_checks"]):
        raise RuntimeError("R0.74S Step 16 dependency boundary drift")
    if step16["claim_boundary"] != {
        "Q1": "OPEN", "Q12": "OPEN",
        "S342_quadratic_tail_for_p_gt_1": "FALSE_BY_SMOOTH_EXACT_NSE",
        "S444_critical_L1_tail": "OPEN",
        "hybrid_terminal_flux_gate": "OPEN_NOT_REFUTED",
        "millennium_problem_solved": False, "regularity": "OPEN",
    }:
        raise RuntimeError("R0.74S Step 16 claim boundary drift")
    step17 = json.loads((ROOT / "research/r074s_recurrent_streamline_certificate.json").read_text(encoding="utf-8"))
    if step17.get("verdict") != "PASS":
        raise RuntimeError("R0.74S Step 17 certificate verdict drift")
    if len(step17["finite_checks"]) != 12 or sum(row["cases"] for row in step17["finite_checks"]) != 4325:
        raise RuntimeError("R0.74S Step 17 finite inventory drift")
    if len(step17["structural_checks"]) != 11 or not all(row["pass"] for row in step17["structural_checks"]):
        raise RuntimeError("R0.74S Step 17 structural boundary drift")
    if len(step17["dependency_checks"]) != 2 or not all(row["pass"] for row in step17["dependency_checks"]):
        raise RuntimeError("R0.74S Step 17 dependency boundary drift")
    if step17["claim_boundary"] != {
        "Q1": "OPEN", "Q12": "OPEN",
        "S342_supercritical_temporal_tail": "FALSE_BY_SMOOTH_EXACT_NSE",
        "S444_critical_L1_temporal_tail": "FALSE_BY_RECURRENT_SMOOTH_EXACT_NSE",
        "S472_fixed_deletion_positive_excursion": "OPEN",
        "absolute_tail_beta_below_one_all_p_at_least_one": "FALSE",
        "direct_hybrid_terminal_flux_gate": "OPEN_NOT_REFUTED",
        "millennium_problem_solved": False, "regularity": "OPEN",
    }:
        raise RuntimeError("R0.74S Step 17 claim boundary drift")


def inline_markup(value: str) -> str:
    value = html.escape(" ".join(value.split()))
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def report_body() -> str:
    source = "\n\n".join([
        (ROOT / "research/r074s_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step13_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step14_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step15_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step16_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step17_report-source.md").read_text(encoding="utf-8").strip(),
    ])
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 0
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(lines[0][3:])}</h2>')
            section_open = True
            continue
        if lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(line.startswith("- ") or line.startswith("  ") for line in lines):
            items, current = [], ""
            for line in lines:
                if line.startswith("- "):
                    if current:
                        items.append(current)
                    current = line[2:]
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            output.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
            continue
        output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    return "\n".join(output)


def render_note() -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="同一 Taylor 光滑精确解的闭流线复现使绝对时间变差达到 A³，并否定所有 beta 小于 1 的 power-only tail，包括 S.444；signed excursion 仍为 A²">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74s.html"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}.hero-inner>div:first-child>p strong{{margin-left:.25em}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}.files{{line-height:2}}.note{{color:var(--muted);font-size:.94rem}}picture img{{display:block;width:100%;height:auto}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem;break-after:avoid}}#figure{{break-before:page}}a{{color:inherit;text-decoration:none}}a[href]::after{{content:none!important}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74S · STEP 17 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74S · Step 17 完整中文版本</div><h1>{TITLE}</h1><p>同一 Taylor 1923 光滑精确解在 regular closed streamline 上产生 \\(O_R(A)\\) 次复现：absolute temporal variation 逐圈累积到 \\(A^3\\)，而 signed positive excursion 仍只有 \\(A^2\\)。 <strong>因此所有 \\(p\\ge1\\)、所有 \\(\\beta&lt;1\\) 的 power-only absolute tail 都为 FALSE，包括 S.444；S.472、direct hybrid gate、S.407、Q.12、Q.1 与正则性仍 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">SMOOTH EXACT NSE</span><span class="label">CLOSED-ORBIT RECURRENCE</span><span class="label">ABSOLUTE VARIATION A³</span><span class="label">SIGNED EXCURSION A²</span><span class="label">FALSE S.444</span><span class="label">OPEN S.472 / S.407</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74S STEP 17</strong><p>S.445–S.475：PROVED / FALSE / OPEN</p><p>Step 16 separatrix absolute variation：\\(A^2\\)</p><p>Step 17 recurrent absolute variation：\\(A^3\\)</p><p>complete payment：\\(A^3\\)</p><p>signed positive excursion：\\(A^2\\)</p><p>all power-only \\(\\beta&lt;1\\)：FALSE</p><p>S.444：FALSE</p><p>S.472 / direct hybrid / S.407：OPEN</p><p>Q.12 / Q.1：OPEN</p><p>regularity / Millennium：OPEN</p><p>解析可视化 · 非 simulation / DNS · NO DGX</p></div></div></header><article>
{report_body()}
<section id="figure"><div class="section-no">F / 期刊级四联图</div><h2>闭流线复现：signed excursion 与 absolute temporal variation</h2><picture><source srcset="/assets/r074s/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074s/{FIGURE_ID}.png" alt="R0.74S Step 17 four-panel analytic visualization of a recurrent Taylor streamline, signed excursion, absolute variation, and amplitude classes"></picture><p><a href="/assets/r074s/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074s/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074s/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074s/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074s/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074s/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074s/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">四个 panel 来自精确 Taylor family、closed-orbit ODE 与冻结公式的 deterministic rendering。它不是 DNS，不是数值 Navier--Stokes simulation，也不是 regularity / Clay 证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 17 主文、三份审计与双语言证书</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_temporal_tail_obstruction.md">recurrent-streamline 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_literature_audit.md">literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_certificate.json">Python 证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_recurrent_streamline_independent_report.md">Ruby 独立 report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074s_recurrent_streamline_certificate.py">Python 复现脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074s_recurrent_streamline_independent.rb">Ruby 独立脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_step17_report-source.md">Step 17 中文 reader source</a></p><p><a href="/notes/r0-74s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74s.html">重大路线修正 recap（R0.61–R0.74S，161 节）</a> · <a href="/recap-r0-61-r0-74s.pdf">recap PDF</a></p><p class="note">Step 17：Python 12/12 finite groups（4,325 cases）、11/11 structural checks、2/2 dependency locks；独立 Ruby 7/7 exact groups（294 assertions）、4/4 artifact locks、20/20 semantic checks、32/32 statement/environment mutations、3/3 path substitutions 与 14/14 reproducibility assertions 全部 PASS。有限证书不替代 continuum proof。</p></section>
<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一节与下一接口</h2><p><a href="/notes/r0-74r.html">← 上一节：R0.74R 终端窗口与任意时钟提取门</a> · <a href="#next">下一接口：R0.74T 尚未启动 →</a></p></section>
<section id="next"><div class="section-no">NEXT / 本次不启动</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">R0.74T / signed endpoint functional 接口</h2><p style="margin:.15rem 0">本次仅发布 R0.74S Step 17，并在此停止。后续若另行启动，只能研究 OPEN S.472、fixed-deletion simultaneous height、direct hybrid last-exit increments、OPEN S.407 或其他明确的新 PDE 输入；不得继续假设已经为 FALSE 的 S.342 或 S.444，也不得把 Q.12、Q.1、正则性或 Millennium 问题写成 theorem。</p></section></article></main></body></html>'''


def copy_figures() -> None:
    source = ROOT / "figures/r074s" / FIGURE_ID
    for target in (PUBLIC / "figures/r074s" / FIGURE_ID, ROOT / "research/figures/r074s" / FIGURE_ID):
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074s"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", assets / f"{FIGURE_ID}.{extension}")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.95"', 'data-site-version="1.96"', "home version"),
        ('/i18n-en.js?v=1.95', '/i18n-en.js?v=1.96', "home i18n"),
        ('/site-refresh.js?v=1.95.1', '/site-refresh.js?v=1.96.1', "home refresh"),
        ('<strong>v1.95</strong>网页版本', '<strong>v1.96</strong>网页版本', "home stat version"),
        ('<h3>R0.74S：Taylor 1923 涡、移动漂移与临界时间端点</h3>', '<h3>R0.74S：闭流线复现与绝对时间尾 no-go</h3>', "current route title"),
        ('<p class="tree-current-summary">Taylor 1923 光滑精确解的 fixed-frame Bernoulli 通量为零，但 Version-M moving drift 使 S.342 对每个 p&gt;1 为 FALSE；临界 S.444 与 S.407 仍 OPEN。NOT CLAY。</p>', '<p class="tree-current-summary">同一 Taylor 光滑精确解的闭轨道复现使 absolute variation 与 complete payment 同为 A³，因此 S.444 及全部 beta&lt;1 power-only tails 为 FALSE；signed excursion 仍为 A²，S.472、direct hybrid 与 S.407 仍 OPEN。NOT CLAY。</p>', "current route summary"),
        ('Taylor 1923 exact vortex → fixed-frame Bernoulli cancellation → Version-M moving drift → S.342 false for p&gt;1 → S.444 / S.407 open</p>', 'Taylor exact vortex → special separatrix A² → closed-orbit recurrence → absolute variation A³ / signed excursion A² → S.444 false → S.472 / direct hybrid / S.407 open</p>', "current route path"),
        ('综述 v1.95 · 2026-09-03', '综述 v1.96 · 2026-09-03', "footer"),
    )
    for old, new, label in pairs:
        page = replace_once_or_present(page, old, new, label)
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74S Step 17 已证否全部 beta&lt;1 的 power-only absolute temporal tails，包括 S.444；研究目标转向 fixed-deletion positive excursion / simultaneous height 或 direct hybrid increments。S.407、Q.12、Q.1 与正则性仍 OPEN。</span></div>', page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74S · 2026-09-03 · STEP 17</p><h2 class="route-map-title" id="latest-release-title">R0.74S｜闭流线复现否定所有次线性绝对时间尾</h2><p class="route-map-intro">同一 Taylor 光滑精确解的闭流线 recurrence 把 absolute variation 从 Step 16 特殊路径的 A² 提升到 A³，而 signed excursion 仍为 A²；S.444 因而为 FALSE。S.472、direct hybrid 与 S.407 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74s.pdf">阅读最新 R0.74S 研究笔记 →</a><a href="/assets/r074s/fig-r074s-recurrent-tail-obstruction.pdf">Step 17 期刊级四联图</a><a href="/recap-r0-61-r0-74s.html">最新重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">221 篇研究笔记总索引</a><a href="#r074s">查看首页 R0.74S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74S · 123 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>98 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74S Step 17</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page, count = re.subn(r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">未启动</span></div><h3>R0.74T signed endpoint functional</h3><p>若另行启动：只研究 OPEN S.472、fixed-deletion simultaneous height、direct hybrid last-exit increments、OPEN S.407 或其他明确的新 PDE input；不得继续假设 FALSE S.342 / S.444。本次仅发布 R0.74S Step 17。</p></article></div>', page, count=1)
    if count != 1:
        raise RuntimeError("next route replacement failed")
    card = '''          <div class="task-one" id="r074s" data-release="r074s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74S Step 17 · 2026-09-03</p><h3>R0.74S｜闭流线复现否定所有次线性绝对时间尾</h3><p>闭轨道 recurrence 使 absolute variation 与 payment 同为 A³，故 S.444 及全部 beta&lt;1 power-only tails 为 FALSE；signed excursion 仍为 A²。S.472、direct hybrid、S.407、Q.1 与正则性仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74s.pdf">PDF</a> · <a href="/assets/r074s/fig-r074s-recurrent-tail-obstruction.pdf">期刊级四联图</a> · <a href="/recap-r0-61-r0-74s.html">里程碑 recap</a></p></div>\n'''
    page = re.sub(r'^[ \t]*<div class="task-one" id="r074s" data-release="r074s"[\s\S]*?</div>\n?', "", page, flags=re.M)
    anchor = '          <div class="task-one" id="r074r"'
    if anchor not in page:
        raise RuntimeError("home R card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    recap = '''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">重大路线修正回顾 R0.61–R0.74S · 2026-09-03</p><h3>R0.60 recap 之后的累计回顾收录 161 个节点；全站现有 221 篇公开研究笔记</h3><p>Step 16 的特殊 separatrix 路径只看到 A²；Step 17 在同一 Taylor 精确解的闭轨道上利用 recurrence，把 absolute temporal variation 提升到 A³，而 signed excursion 仍保持 A²。</p><p><strong>当前边界：</strong>S.342 与 S.444 均为 FALSE；下一目标转向 fixed-deletion positive excursion / simultaneous height 或 direct hybrid increments。S.407、Q.12、Q.1、正则性与 Clay 仍 OPEN。</p><p><a href="/recap-r0-61-r0-74s.html"><strong>阅读 R0.61–R0.74S 完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-74s.pdf">下载同步 PDF</a></p></div>'''
    page, count = re.subn(r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>', lambda _: recap, page, count=1)
    if count != 1:
        raise RuntimeError("home recap card replacement failed")
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.95"', 'data-site-version="1.96"', "lit version"), ('/i18n-en.js?v=1.95', '/i18n-en.js?v=1.96', "lit i18n"), ('文献综述 v1.95 · 2026-09-03', '文献综述 v1.96 · 2026-09-03', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    new = '<div class="route-step kept"><header><b>R0.74S</b><strong>闭流线复现与绝对时间尾 no-go</strong></header><p>Step 16 的特殊 separatrix 路径给出 A²；Step 17 在同一 Taylor 光滑精确解的 regular closed streamline 上证明 absolute variation 与 complete payment 均为 A³，而 signed excursion 为 A²。因此 S.342、S.444 及全部 beta&lt;1 power-only tails 为 FALSE。<a href="/notes/r0-74s.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">里程碑 recap</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>signed endpoint functional</strong></header><p>研究 OPEN S.472、fixed-deletion simultaneous height、direct hybrid increments 或 OPEN S.407；不得恢复 FALSE S.342 / S.444。</p></div>'
    page, count = re.subn(r'<div class="route-step kept"><header><b>R0\.74S</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口 · R0\.74T</b>[\s\S]*?</div>', lambda _: new, page, count=1)
    if count != 1:
        raise RuntimeError("literature route replacement failed")
    boundary = '<h3 id="r074s-boundary">R0.74S Step 17 的文献与主张边界</h3><p>Step 17 仍使用 Taylor 1923 的 bi-periodic decaying vortex；closed-streamline recurrence、Version-M path、physical-shell deletion 与 payment comparison 均由直接 substitution 证明，不归因于历史来源。Yang 的 skewed cylinders、Dascaliuc--Grujić 的 signed averaged flux、Wolf 的 local pressure 与 Duchon--Robert 的 signed local balance 均不控制这里的 absolute recurrent backtracking debt。有限检索不声称 novelty、priority 或 exhaustiveness。</p><div class="boundary"><strong>R0.74S Step 17 公开边界</strong><p>PROVED：S.445–S.475 的 closed-orbit recurrence、A³ absolute tail / complete payment、A² signed excursion 与 completed-clock comparison。FALSE：所有 p≥1、所有 beta&lt;1 的 power-only absolute temporal tail，包括 S.444。FINITE：Python 12/12 groups（4,325 cases）；independent Ruby 7/7 exact groups（294 assertions），所有 mutation/path/reproducibility checks 通过。OPEN：S.472、direct hybrid gate、S.407、Q.12、Q.1、scale contraction 与 regularity。图为 analytic exact-field visualization，不是 DNS 或数值 NSE simulation。<strong>NOT CLAY.</strong> <a href="/notes/r0-74s.html">阅读完整中文笔记</a> · <a href="/recap-r0-61-r0-74s.html">阅读路线修正 recap</a>。</p></div>\n'
    page = re.sub(r'<h3 id="r074s-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?', "", page)
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_notes_index() -> None:
    target = PUBLIC / "notes/index.html"
    page = target.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.95"', 'data-site-version="1.96"', "index version"), ('/i18n-en.js?v=1.95', '/i18n-en.js?v=1.96', "index i18n"), ('/site-refresh.js?v=1.95', '/site-refresh.js?v=1.96', "index refresh"), ('研究笔记总索引 · v1.95 · 2026-09-03', '研究笔记总索引 · v1.96 · 2026-09-03', "index footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    entry = '''          <li class="note-entry" data-note="r0-74s"><article><div class="entry-copy"><p class="note-code">R0.74S · STEP 17</p><h3>闭流线复现否定所有次线性绝对时间尾</h3></div><nav class="entry-files" aria-label="R0.74S files"><a class="file-link html" href="/notes/r0-74s.html" aria-label="Read R0.74S HTML">HTML</a><a class="file-link pdf" href="/notes/r0-74s.pdf" aria-label="Download R0.74S PDF">PDF</a></nav></article></li>\n'''
    anchor = '          <li class="note-entry" data-note="r0-74r">'
    page, existing = re.subn(r'\s*<li class="note-entry" data-note="r0-74s">[\s\S]*?</li>\n?', "\n" + entry, page, count=1)
    if existing == 0:
        if anchor not in page:
            raise RuntimeError("index R anchor missing")
        page = page.replace(anchor, entry + anchor, 1)
    write_text(target, page)


def route_post_r060_count(page: str) -> int:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end])
    return len(slugs) - slugs.index("r0-61")


def post_r060_slugs(page: str) -> list[str]:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    return ordered[ordered.index("r0-61"):]


def render_recap() -> str:
    slugs = post_r060_slugs(HOME.read_text(encoding="utf-8"))
    if len(slugs) != 161 or slugs[0] != "r0-61" or slugs[-1] != "r0-74s":
        raise RuntimeError(f"Step 17 recap route coverage drift: {len(slugs)} {slugs[:1]} {slugs[-1:]}")
    links = "\n".join(f'<a href="/notes/{slug}.html">{slug[3:].upper()}</a>' for slug in slugs)
    return rf'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>R0.61–R0.74S 重大路线修正回顾｜从 scalar no-go 到 signed endpoint functional</title>
<meta name="description" content="R0.61 至 R0.74S 的 161 节累计回顾：Step 16 separatrix 的 A² 与 Step 17 recurrence 的 A³ 分野，以及 fixed-deletion simultaneous-height 新接口">
<link rel="canonical" href="https://kasifa.github.io/recap-r0-61-r0-74s.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 Georgia,"Songti SC","Noto Serif SC",serif}}nav{{padding:12px 5vw;border-top:5px solid var(--ink);border-bottom:3px double var(--ink);display:flex;justify-content:space-between;gap:1rem}}main{{width:min(980px,90vw);margin:auto}}header{{padding:55px 0 30px;border-bottom:1px solid var(--line)}}h1{{font-size:clamp(2rem,5vw,3.7rem);line-height:1.08}}h2{{color:var(--rule);margin-top:2.4rem}}section{{border-bottom:1px dotted var(--line);padding-bottom:1rem}}.eyebrow{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.06em;text-transform:uppercase}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.card,.boundary{{background:var(--raised);border:1px solid var(--line);padding:1rem 1.2rem}}.node-links{{display:flex;flex-wrap:wrap;gap:.45rem}}.node-links a{{border:1px solid var(--line);padding:.2rem .45rem;text-decoration:none}}a{{color:var(--rule)}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{body{{font-size:15px}}.grid{{grid-template-columns:1fr}}nav{{font-size:13px}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}nav{{display:none}}body{{font-size:9pt}}main{{width:auto}}header{{padding-top:0}}.card{{break-inside:avoid}}}}</style></head>
<body><nav><a href="/research-review.html">研究首页</a><span>R0.61–R0.74S · 2026-09-03</span></nav><main><header><p class="eyebrow">MAJOR ROUTE-CORRECTION RECAP · 161 NODES</p><h1>从 scalar no-go 到 signed endpoint functional</h1><p>这是 R0.60 之后第三份累计回顾。收录节点：161；回顾截止时公开笔记：221。它保留 R0.61–R0.74O 的旧 recap 字节不变，并新增 R0.74P–R0.74S 四个研究节点；R0.74S 内只在此次重大路线修正时更新一次 recap。</p><p><a href="/recap-r0-61-r0-74s.pdf">下载同步累计回顾 PDF</a> · <a href="/notes/r0-74s.html">阅读 R0.74S Step 17</a> · <a href="/recap-r0-61-r0-74o.html">上一版里程碑 recap</a></p></header>
<article><section id="retained"><p class="eyebrow">01 / 保留历史主干</p><h2>R0.61–R0.74O 的证明、反例与开放边界保持原量词</h2><p>旧节点从 projected-Lamb 热体积、局部热 packing、精确 shear 与谱分支，推进到 suitable-weak moving tube、\(\mathcal V\in L_t^1\) 时钟账本、\(2K^2\) 阈值、完整 payment、全壳合成和自由被动振幅的 scalar-payment-only no-go。R0.74O 已证明冻结标量支付本身不足；它没有预言哪一个 temporal functional 能闭合，也没有改变 regularity / Clay 的 OPEN 状态。</p></section>
<section><p class="eyebrow">02 / P–R 过渡</p><h2>从增广可观测量筛选到 terminal clock extraction</h2><div class="grid"><div class="card"><h3>R0.74P｜时间可观测量筛选</h3><p>固定正阶窗口会漏检；defect-completed shell clock 在固定尺度 suitable-weak 极限下稳定，但 matching square-function 上界仍开放。</p></div><div class="card"><h3>R0.74Q｜有效壳层与三次 payment</h3><p>terminal best-N 归约成立；共同剪切多包能同时点亮目标壳层，却被最外真实 velocity-cubic payment 阻断。</p></div><div class="card"><h3>R0.74R｜任意时钟提取门</h3><p>凸 payment 强迫第一壳层集中；任意 completed clock 的耗散、动能窗口与近期正变差三分法成立，persistence packing 仍开放。</p></div><div class="card"><h3>R0.74S｜从 clocks 到 signed flux</h3><p>连续 17 个 step 把正时钟、终端窗口、common deletion、crown 与 temporal tail 逐层审计，最终由 exact Taylor family 识别 absolute variation 的根本障碍。</p></div></div></section>
<section><p class="eyebrow">03 / 决定性修正</p><h2>Step 16 的 A² 没有错；错的是把特殊 separatrix 外推成 universal endpoint</h2><p>Step 16 选取非复现 invariant line 上的 terminal centre。轨迹只穿过关键相位一次，所以对该 terminal setting，critical \(p=1\) absolute variation 恰为 \(A^2\)，payment 为 \(A^3\)。这只能证明 exponent compatibility，不能判定对所有 terminal settings 量化的 S.444。</p><p>Step 17 在同一光滑 Taylor 精确解上改取 regular closed streamline。固定物理时间窗内出现 \(O_R(A)\) 次 recurrence；absolute variation 逐圈累计到 \(A^3\)，complete payment 仍为 \(A^3\)。因此所有 \(p\ge1\)、所有 \(\beta&lt;1\) 的 power-only absolute tails 都失败，S.444 随之成为 FALSE。</p></section>
<section><p class="eyebrow">04 / 正确保留的信息</p><h2>signed excursion 仍是 A²；研究目标转向 fixed-deletion hybrid / simultaneous height</h2><p>同一 recurrent family 的 signed range 与 positive excursion 仍只有 \(A^2\)。Jordan identity 把 total variation 分成 terminal endpoint 与两倍 backtracking debt；被 absolute value 反复收费的是每圈上下往返，而 Step 15 的 terminal hybrid coordinate 只需要两个时刻之间的 signed increment。</p><p>因此下一充分输入是 OPEN S.472 的 fixed-deletion positive excursion，或等价到已支付 Q-variation 的 simultaneous maximal-height clock estimate。更弱的 direct hybrid last-exit gate 也仍 OPEN。terminal-crown coercivity S.407、Q.12、Q.1、scale contraction 与 regularity 没有被这次 no-go 关闭。下一接口 R0.74T 尚未启动。</p></section>
<section><p class="eyebrow">05 / 证据等级</p><h2>解析结论、有限复算、图面与文献边界继续分开</h2><div class="boundary"><p><strong>PROVED：</strong>closed-orbit recurrence、A³ absolute tail、A³ complete payment、A² signed excursion、BV 与 completed-clock comparisons。</p><p><strong>FALSE：</strong>S.342、S.444，以及所有 beta&lt;1 的 power-only absolute temporal tails。</p><p><strong>FINITE：</strong>Python 4,325 cases 与独立 Ruby 294 exact assertions 加 mutation/path/reproducibility checks；不替代 continuum proof。</p><p><strong>VISUAL：</strong>四联图是 exact-field deterministic rendering，不是 DNS 或数值 NSE simulation。</p><p><strong>LITERATURE BOUNDARY：</strong>有限一手来源检查不证明 novelty、priority 或 exhaustiveness。</p><p><strong>OPEN / NOT CLAY：</strong>S.472、direct hybrid、S.407、Q.12、Q.1 与 regularity 仍开放；没有奇点构造或 Millennium 结论。</p></div></section>
<section id="node-index"><p class="eyebrow">NODE INDEX / 161</p><h2>R0.61–R0.74S 全部节点</h2><div class="node-links">{links}</div></section></article></main></body></html>'''


def update_accounting() -> None:
    html_count = sum(" 2.html" not in path.name for path in (PUBLIC / "notes").glob("r0-*.html"))
    pdf_count = sum(" 2.pdf" not in path.name for path in (PUBLIC / "notes").glob("r0-*.pdf")) + (0 if (PUBLIC / "notes/r0-74s.pdf").exists() else 1)
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "latestPublishedResearchHtml": "/notes/r0-74s.html", "latestPublishedResearchPdf": "/notes/r0-74s.pdf", "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03"})
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if RELEASE not in inventory[key]:
            inventory[key].append(RELEASE)
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    inventory["sameReleaseCompletedSteps"] = {"r074s": 17}
    inventory["formalFigureExemptReleaseCount"] = len(inventory.get("formalFigureExemptReleases", []))
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({"latestCompletedRelease": RELEASE, "latestCompletedStep": 17, "siteVersion": VERSION, "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161, "nextRelease": "r074t", "latestPublishedResearchHtml": "/notes/r0-74s.html", "latestPublishedResearchPdf": "/notes/r0-74s.pdf", "latestReleaseGate": "tests/r074s-step17-gate.test.mjs", "latestReleasePublicationTest": "tests/r074s-step17-release.test.mjs", "postR070APublishedReleaseCount": inventory["publishedReleaseCount"], "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"], "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "latestRecapRelease": "r074s", "latestRecapHtml": "/recap-r0-61-r0-74s.html", "latestRecapPdf": "/recap-r0-61-r0-74s.pdf", "latestReleaseTranslationScript": "scripts/add-r074s-translations.mjs", "latestReleaseStepTranslationScript": "scripts/add-r074s-step17-translations.mjs", "latestReleasePdfBinder": "scripts/bind-r074s-step17-pdf.mjs", "recapPolicy": "MILESTONE_ONLY"})
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_sources()
    assert_recap()
    write_text(PUBLIC / "notes/r0-74s.html", render_note())
    if "--note-only" not in sys.argv:
        copy_figures(); update_home(); update_literature(); write_text(PUBLIC / "recap-r0-61-r0-74s.html", render_recap()); update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        update_notes_index()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "formalFigure": FIGURE_ID, "simulation": False, "dgxUsed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
