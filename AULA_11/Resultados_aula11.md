Execução 1 — Suíte completa (sem erro)
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content/AULA_11
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.62s ===============================

============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content/AULA_11
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto FAILED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

=================================== FAILURES ===================================

♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ERRO PROPOSITAL♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

_________________________ test_monotonicidade_impacto __________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f53b830f4d0>

    def test_monotonicidade_impacto(simulador):
        """Aumentar o impacto mantendo a explorabilidade deve AUMENTAR ou MANTER a urgencia."""
        exp_fixa = 5.0
        urg_baixa = executar_inferencia(simulador, 20.0, exp_fixa)
        urg_media = executar_inferencia(simulador, 50.0, exp_fixa)
        urg_alta = executar_inferencia(simulador, 90.0, exp_fixa)
    
        # ERRO PROPOSITAL: invertida a logica, exigindo que a urgencia DIMINUA
        # conforme o impacto aumenta - o oposto do comportamento real do sistema.
>       assert urg_baixa >= urg_media >= urg_alta, (
            f"Violacao de Monotonicidade: {urg_baixa:.1f} >= {urg_media:.1f} >= {urg_alta:.1f}"
        )
E       AssertionError: Violacao de Monotonicidade: 11.7 >= 76.7 >= 92.2
E       assert np.float64(11.666666666666664) >= np.float64(76.66666666666666)

test_fuzzy_engine.py:49: AssertionError
=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_monotonicidade_impacto - AssertionError: Violacao de Monotonicidade: 11.7 >= 76.7 >= 92.2
========================= 1 failed, 3 passed in 1.83s ==========================

♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦CORREÇÃO♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦

============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content/AULA_11
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.57s ===============================
