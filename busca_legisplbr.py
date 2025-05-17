import sys
import time
import pandas as pd
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QFileDialog, QComboBox, QTextEdit, QMessageBox, QGroupBox, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt

from tramitacao import obter_proposicoes, obter_autores, obter_tramitacao, obter_status_proposicao, obter_keywords
from transformacao import (
    foi_aprovado, foi_finalizado, mapear_categoria_tema,
    extrair_uf_principal, mapear_regiao,
    extrair_partido_principal, classificar_bloco_partidario
)

class ProposicaoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Busca de Proposições - Câmara dos Deputados")
        self.setGeometry(100, 100, 1100, 750)
        self.df = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        filters_layout = QHBoxLayout()

        # Filtros de busca e enriquecimento lado a lado
        self.filter_box = self.create_filter_group()
        self.enrichment_box = self.create_enrichment_filter_group()
        filters_layout.addWidget(self.filter_box)
        filters_layout.addWidget(self.enrichment_box)
        main_layout.addLayout(filters_layout)

        # Botões principais
        btn_layout = QHBoxLayout()
        self.btn_buscar = QPushButton("Buscar")
        self.btn_enriquecer = QPushButton("Enriquecer")
        self.btn_salvar = QPushButton("Salvar")
        self.btn_limpar = QPushButton("Limpar todos os filtros")
        self.btn_enriquecer.setEnabled(False)
        self.btn_salvar.setEnabled(False)

        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_enriquecer.clicked.connect(self.enriquecer)
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_limpar.clicked.connect(self.limpar_todos_os_filtros)

        btn_layout.addWidget(self.btn_buscar)
        btn_layout.addWidget(self.btn_enriquecer)
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_limpar)
        main_layout.addLayout(btn_layout)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)

    def create_filter_group(self):
        group = QGroupBox("Filtros de Busca")
        layout = QVBoxLayout()

        self.chk_tipo = [QCheckBox(t) for t in ["PL", "PEC", "PLP", "MPV"]]
        self.chk_ano = [QCheckBox(str(a)) for a in range(2020, int(datetime.datetime.now().year)+1)]

        todos_ufs = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB",
                     "PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
        todos_partidos = sorted(set([
            "PT", "PSOL", "PCdoB", "REDE", "PSB", "PDT", "PV", "MDB", "PSD", "PP", "PL", "Republicanos",
            "União Brasil", "Avante", "Podemos", "Solidariedade", "Patriota", "PROS", "Novo", "PSC", "DEM", "PSL", "PRTB"
        ]))

        self.chk_estado = [QCheckBox(uf) for uf in todos_ufs]
        self.chk_partido = [QCheckBox(p) for p in todos_partidos]

        self.grupos_filtros = [self.chk_tipo, self.chk_ano, self.chk_estado, self.chk_partido]

        for label, chks in zip(["Tipo:", "Ano:", "UF:", "Partido:"], self.grupos_filtros):
            mark_all = QCheckBox("[Marcar todos]")
            mark_all.setStyleSheet("color: green; font-weight: bold")
            layout.addWidget(QLabel(label))
            layout.addWidget(mark_all)
            grid = QGridLayout()
            for i, cb in enumerate(chks):
                grid.addWidget(cb, i // 6, i % 6)
            layout.addLayout(grid)

            def toggle_all(state, checkboxes=chks):
                for cb in checkboxes:
                    cb.setChecked(state == Qt.Checked)

            mark_all.stateChanged.connect(lambda state, checkboxes=chks: toggle_all(state, checkboxes))

        group.setLayout(layout)
        return group

    def create_enrichment_filter_group(self):
        group = QGroupBox("Filtros de Enriquecimento")
        layout = QVBoxLayout()

        campos = [
            "aprovado", "finalizado", "dias_tramitacao", "tema_dominante",
            "uf_principal", "região", "partido_principal", "bloco_partidario",
            "apensada_ou_duplicada", "autoria_coletiva", "qtd_tramitacoes"
        ]
        self.chk_enriquecer = [QCheckBox(campo) for campo in campos]

        mark_all = QCheckBox("[Marcar todos]")
        mark_all.setStyleSheet("color: green; font-weight: bold")
        layout.addWidget(QLabel("Campos para enriquecer:"))
        layout.addWidget(mark_all)

        grid = QGridLayout()
        for i, cb in enumerate(self.chk_enriquecer):
            grid.addWidget(cb, i // 2, i % 2)
        layout.addLayout(grid)

        def toggle_all(state):
            for cb in self.chk_enriquecer:
                cb.setChecked(state == Qt.Checked)

        mark_all.stateChanged.connect(toggle_all)

        group.setLayout(layout)
        return group

    def limpar_todos_os_filtros(self):
        for grupo in self.grupos_filtros + [self.chk_enriquecer]:
            for cb in grupo:
                cb.setChecked(False)
    def buscar(self):
        tipos = [cb.text() for cb in self.chk_tipo if cb.isChecked()]
        anos = [int(cb.text()) for cb in self.chk_ano if cb.isChecked()]

        if not tipos or not anos:
            QMessageBox.warning(self, "Erro", "Selecione ao menos um tipo e um ano.")
            return

        self.log_output.append("Iniciando busca...")
        todas = []
        for tipo in tipos:
            for ano in anos:
                self.log_output.append(f"Buscando proposições {tipo} de {ano}...")
                proposicoes = obter_proposicoes(ano=ano, sigla_tipo=tipo)
                num_proposicoes = len(proposicoes)
                self.log_output.append(f"Achadas {num_proposicoes} proposições...")
                i = 1
                for prop in proposicoes:
                    self.log_output.append(f"Agregando valores a proposição de ID {prop['id']}... {i} de {num_proposicoes}")
                    i = i + 1
                    QApplication.processEvents()

                    autor_info = obter_autores(prop["id"])
                    prop["autores"] = autor_info["autores"]
                    prop["tipo de autor"] = autor_info["tipo_autor"]

                    tram = obter_tramitacao(prop["id"])
                    prop.update({
                        "órgão inicial": tram["orgao_inicial"],
                        "descrição inicial": tram["descricao_inicial"],
                        "data da apresentação": tram["data_inicial"],
                        "último órgão": tram["orgao_ultimo"],
                        "última tramitação": tram["descricao_ultimo"],
                        "data da última tramitação": tram["data_ultimo"]
                    })

                    prop["status atual"] = obter_status_proposicao(prop["id"])
                    prop["temas"] = obter_keywords(prop["id"])

                    time.sleep(0.4)
                todas.extend(proposicoes)


        df = pd.DataFrame(todas)

        ufs_filtradas = [cb.text() for cb in self.chk_estado if cb.isChecked()]
        partidos_filtrados = [cb.text() for cb in self.chk_partido if cb.isChecked()]

        # Aplicar filtro por UF, se houver
        if ufs_filtradas:
            df["uf_principal"] = df["autores"].apply(extrair_uf_principal)
            df = df[df["uf_principal"].isin(ufs_filtradas)]
            self.log_output.append(f"Filtrando por UFs: {ufs_filtradas}")
            if df.empty:
                QMessageBox.information(self, "Sem resultados",
                                        "Nenhuma proposição encontrada com as UFs selecionadas.")
                return

        # Aplicar filtro por Partido, se houver
        if partidos_filtrados:
            df["partido_principal"] = df["autores"].apply(extrair_partido_principal)
            df = df[df["partido_principal"].isin(partidos_filtrados)]
            self.log_output.append(f"Filtrando por Partidos: {partidos_filtrados}")
            if df.empty:
                QMessageBox.information(self, "Sem resultados",
                                        "Nenhuma proposição encontrada com os partidos selecionados.")
                return

        self.df = df.reset_index(drop=True)
        self.btn_enriquecer.setEnabled(True)
        self.btn_salvar.setEnabled(True)
        self.log_output.append("Busca concluída.")

    def enriquecer(self):
        if self.df is None:
            return

        self.log_output.append("Aplicando transformações...")
        df = self.df
        campos = [cb.text() for cb in self.chk_enriquecer if cb.isChecked()]

        if "aprovado" in campos:
            df["aprovado"] = df["status atual"].apply(foi_aprovado)
        if "finalizado" in campos:
            df["finalizado"] = df["status atual"].apply(foi_finalizado)
        if "dias_tramitacao" in campos:
            df["dias_tramitacao"] = (
                pd.to_datetime(df["data da última tramitação"], errors="coerce") -
                pd.to_datetime(df["data da apresentação"], errors="coerce")
            ).dt.days
        if "tema_dominante" in campos:
            df["tema_dominante"] = df["temas"].apply(mapear_categoria_tema)
        if "uf_principal" in campos:
            df["uf_principal"] = df["autores"].apply(extrair_uf_principal)
        if "região" in campos:
            df["região"] = df["uf_principal"].apply(mapear_regiao)
        if "partido_principal" in campos:
            df["partido_principal"] = df["autores"].apply(extrair_partido_principal)
        if "bloco_partidario" in campos:
            df["bloco_partidario"] = df["partido_principal"].apply(classificar_bloco_partidario)
        if "apensada_ou_duplicada" in campos:
            df["apensada_ou_duplicada"] = df.duplicated(subset="ementa", keep=False)
        if "autoria_coletiva" in campos:
            df["autoria_coletiva"] = df["autores"].apply(lambda x: isinstance(x, str) and ("," in x))
        if "qtd_tramitacoes" in campos:
            df["qtd_tramitacoes"] = df.apply(lambda row: 1 if row["data da apresentação"] == row["data da última tramitação"] else 2, axis=1)

        self.df = df
        self.log_output.append("Transformações aplicadas.")

    def salvar(self):
        if self.df is None:
            QMessageBox.warning(self, "Erro", "Nenhum dado disponível para salvar.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Excel Files (*.xlsx)")
        if path:
            try:
                self.df.to_excel(path, index=False)
                self.log_output.append(f"Arquivo salvo em: {path}")
            except PermissionError:
                QMessageBox.critical(self, "Erro ao Salvar",
                                     "Não foi possível salvar o arquivo. Verifique se ele está aberto em outro programa e tente novamente.")
            except Exception as e:
                QMessageBox.critical(self, "Erro ao Salvar",
                                     f"Erro inesperado ao salvar o arquivo:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProposicaoApp()
    window.show()
    sys.exit(app.exec_())
