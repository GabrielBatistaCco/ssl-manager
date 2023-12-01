import axios from 'axios';
import { toast } from 'vue3-toastify';
import { m as makeComponentProps, u as useRender, V as VBtn } from './index-813ed69d.mjs';
import { ref, createVNode, resolveDirective, withCtx, openBlock, createBlock, createCommentVNode, mergeProps, withDirectives, createTextVNode, useSSRContext } from 'vue';
import { ssrRenderComponent, ssrGetDirectiveProps } from 'vue/server-renderer';
import { p as propsFactory, g as genericComponent, _ as _export_sfc } from '../server.mjs';
import { m as makeFormProps, c as createForm, f as forwardRefs, V as VContainer, a as VRow, b as VCol, d as VTextField } from './VTextField-6f099a85.mjs';
import '../../nitro/node-server.mjs';
import 'node:http';
import 'node:https';
import 'fs';
import 'path';
import 'node:fs';
import 'node:url';
import 'unhead';
import '@unhead/shared';
import 'vue-router';

const makeVFormProps = propsFactory({
  ...makeComponentProps(),
  ...makeFormProps()
}, "VForm");
const VForm = genericComponent()({
  name: "VForm",
  props: makeVFormProps(),
  emits: {
    "update:modelValue": (val) => true,
    submit: (e) => true
  },
  setup(props, _ref) {
    let {
      slots,
      emit
    } = _ref;
    const form = createForm(props);
    const formRef = ref();
    function onReset(e) {
      e.preventDefault();
      form.reset();
    }
    function onSubmit(_e) {
      const e = _e;
      const ready = form.validate();
      e.then = ready.then.bind(ready);
      e.catch = ready.catch.bind(ready);
      e.finally = ready.finally.bind(ready);
      emit("submit", e);
      if (!e.defaultPrevented) {
        ready.then((_ref2) => {
          var _a;
          let {
            valid
          } = _ref2;
          if (valid) {
            (_a = formRef.value) == null ? void 0 : _a.submit();
          }
        });
      }
      e.preventDefault();
    }
    useRender(() => {
      var _a;
      return createVNode("form", {
        "ref": formRef,
        "class": ["v-form", props.class],
        "style": props.style,
        "novalidate": true,
        "onReset": onReset,
        "onSubmit": onSubmit
      }, [(_a = slots.default) == null ? void 0 : _a.call(slots, form)]);
    });
    return forwardRefs(form, formRef);
  }
});
const _sfc_main = {
  layout: "default",
  name: "editCertificates",
  data() {
    return {
      certificate: {
        id: null,
        domain: null,
        ssls_url: null,
        activation_ssl: null,
        expiration_ssl: null,
        activation_weekday: null,
        expiration_weekday: null,
        issuer: null,
        status_ssl: null
      }
    };
  },
  mounted() {
    var _a, _b;
    if (((_b = (_a = this.$route) == null ? void 0 : _a.params) == null ? void 0 : _b.id) && this.$route.params.id !== "false") {
      this.getCertificate(this.$route.params.id);
    }
  },
  methods: {
    async persistir() {
      try {
        let certificate = {
          domain: this.certificate.domain,
          ssls_url: this.certificate.ssls_url
        };
        if (!this.certificate.id) {
          let response = await axios.post(`${"http://localhost:8000"}/certificates/`, certificate);
          response = response.data.domain;
          toast(`Registro criado com sucesso`, {
            autoClose: 1e3,
            position: "bottom-right",
            theme: "dark"
          });
          this.$router.push("/ssl");
        } else {
          certificate.id = this.certificate.id;
          await axios.put(`${"http://localhost:8000"}/certificates/${certificate.id}/`, certificate);
          toast(`Registro atualizado com sucesso`, {
            autoClose: 1e3,
            position: "bottom-right",
            theme: "dark"
          });
          return this.$router.push("/ssl");
        }
      } catch (error) {
        toast(`Ocorreu um erro no cadastro, contate o administrador`, {
          autoClose: 1e3,
          position: "bottom-right",
          theme: "dark"
        });
      }
    },
    formatDate(date) {
      date = new Date(date);
      if (isNaN(new Date(date).getTime())) {
        return "";
      }
      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      let dateFormtat = `${day < 10 ? "0" : ""}${day}/${month < 10 ? "0" : ""}${month}/${year}`;
      return dateFormtat;
    },
    async getCertificate(id) {
      try {
        let certificate = await axios.get(`${"http://localhost:8000"}/certificates/${id}/`);
        certificate.data.activation_ssl = this.formatDate(certificate.data.activation_ssl);
        certificate.data.expiration_ssl = this.formatDate(certificate.data.expiration_ssl);
        certificate.data.expiration_ssl = this.formatDate(certificate.data.expiration_ssl);
        this.certificate = certificate.data;
      } catch (error) {
        toast(`Ocorreu um erro ao editar o registro, contate o administrador`, {
          autoClose: 1e3,
          position: "bottom-right",
          theme: "dark"
        });
      }
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _directive_value = resolveDirective("value");
  _push(ssrRenderComponent(VContainer, _attrs, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(ssrRenderComponent(VRow, {
          "no-gutters": "",
          class: "py-10 justify-center"
        }, {
          default: withCtx((_2, _push3, _parent3, _scopeId2) => {
            if (_push3) {
              _push3(ssrRenderComponent(VCol, { cols: "6" }, {
                default: withCtx((_3, _push4, _parent4, _scopeId3) => {
                  if (_push4) {
                    if (!$data.certificate.id) {
                      _push4(`<h1 class="text-center pb-5"${_scopeId3}>Cadastro de certificados</h1>`);
                    } else {
                      _push4(`<!---->`);
                    }
                    if ($data.certificate.id) {
                      _push4(`<h1 class="text-center pb-5"${_scopeId3}>Edi\xE7\xE3o de certificados</h1>`);
                    } else {
                      _push4(`<!---->`);
                    }
                  } else {
                    return [
                      !$data.certificate.id ? (openBlock(), createBlock("h1", {
                        key: 0,
                        class: "text-center pb-5"
                      }, "Cadastro de certificados")) : createCommentVNode("", true),
                      $data.certificate.id ? (openBlock(), createBlock("h1", {
                        key: 1,
                        class: "text-center pb-5"
                      }, "Edi\xE7\xE3o de certificados")) : createCommentVNode("", true)
                    ];
                  }
                }),
                _: 1
              }, _parent3, _scopeId2));
              _push3(ssrRenderComponent(VCol, { cols: "8" }, {
                default: withCtx((_3, _push4, _parent4, _scopeId3) => {
                  if (_push4) {
                    _push4(ssrRenderComponent(VForm, {
                      modelValue: _ctx.valid,
                      "onUpdate:modelValue": ($event) => _ctx.valid = $event
                    }, {
                      default: withCtx((_4, _push5, _parent5, _scopeId4) => {
                        if (_push5) {
                          _push5(ssrRenderComponent(VRow, { "no-gutters": "" }, {
                            default: withCtx((_5, _push6, _parent6, _scopeId5) => {
                              if (_push6) {
                                if ($data.certificate.id) {
                                  _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                    default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                      if (_push7) {
                                        _push7(ssrRenderComponent(VTextField, mergeProps({
                                          modelValue: $data.certificate.id,
                                          "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                          disabled: "",
                                          placeholder: "ID",
                                          label: "ID"
                                        }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.id)), null, _parent7, _scopeId6));
                                      } else {
                                        return [
                                          withDirectives(createVNode(VTextField, {
                                            modelValue: $data.certificate.id,
                                            "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                            disabled: "",
                                            placeholder: "ID",
                                            label: "ID"
                                          }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                            [_directive_value, $data.certificate.id]
                                          ])
                                        ];
                                      }
                                    }),
                                    _: 1
                                  }, _parent6, _scopeId5));
                                } else {
                                  _push6(`<!---->`);
                                }
                                _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                  default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                    if (_push7) {
                                      _push7(ssrRenderComponent(VTextField, mergeProps({
                                        modelValue: $data.certificate.domain,
                                        "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                        placeholder: "Dom\xEDnio",
                                        label: "Dom\xEDnio"
                                      }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.domain)), null, _parent7, _scopeId6));
                                    } else {
                                      return [
                                        withDirectives(createVNode(VTextField, {
                                          modelValue: $data.certificate.domain,
                                          "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                          placeholder: "Dom\xEDnio",
                                          label: "Dom\xEDnio"
                                        }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                          [_directive_value, $data.certificate.domain]
                                        ])
                                      ];
                                    }
                                  }),
                                  _: 1
                                }, _parent6, _scopeId5));
                                _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                  default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                    if (_push7) {
                                      _push7(ssrRenderComponent(VTextField, mergeProps({
                                        modelValue: $data.certificate.ssls_url,
                                        "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                        placeholder: "Url ssls",
                                        label: "Url ssls"
                                      }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.ssls_url)), null, _parent7, _scopeId6));
                                    } else {
                                      return [
                                        withDirectives(createVNode(VTextField, {
                                          modelValue: $data.certificate.ssls_url,
                                          "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                          placeholder: "Url ssls",
                                          label: "Url ssls"
                                        }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                          [_directive_value, $data.certificate.ssls_url]
                                        ])
                                      ];
                                    }
                                  }),
                                  _: 1
                                }, _parent6, _scopeId5));
                                if ($data.certificate.activation_ssl) {
                                  _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                    default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                      if (_push7) {
                                        _push7(ssrRenderComponent(VTextField, mergeProps({
                                          modelValue: $data.certificate.activation_ssl,
                                          "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                          disabled: "",
                                          placeholder: "Data da ativa\xE7\xE3o",
                                          label: "Data da ativa\xE7\xE3o"
                                        }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.activation_ssl)), null, _parent7, _scopeId6));
                                      } else {
                                        return [
                                          withDirectives(createVNode(VTextField, {
                                            modelValue: $data.certificate.activation_ssl,
                                            "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                            disabled: "",
                                            placeholder: "Data da ativa\xE7\xE3o",
                                            label: "Data da ativa\xE7\xE3o"
                                          }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                            [_directive_value, $data.certificate.activation_ssl]
                                          ])
                                        ];
                                      }
                                    }),
                                    _: 1
                                  }, _parent6, _scopeId5));
                                } else {
                                  _push6(`<!---->`);
                                }
                                if ($data.certificate.expiration_ssl) {
                                  _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                    default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                      if (_push7) {
                                        _push7(ssrRenderComponent(VTextField, mergeProps({
                                          modelValue: $data.certificate.expiration_ssl,
                                          "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                          disabled: "",
                                          placeholder: "Data expira\xE7\xE3o",
                                          label: "Data expira\xE7\xE3o"
                                        }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.expiration_ssl)), null, _parent7, _scopeId6));
                                      } else {
                                        return [
                                          withDirectives(createVNode(VTextField, {
                                            modelValue: $data.certificate.expiration_ssl,
                                            "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                            disabled: "",
                                            placeholder: "Data expira\xE7\xE3o",
                                            label: "Data expira\xE7\xE3o"
                                          }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                            [_directive_value, $data.certificate.expiration_ssl]
                                          ])
                                        ];
                                      }
                                    }),
                                    _: 1
                                  }, _parent6, _scopeId5));
                                } else {
                                  _push6(`<!---->`);
                                }
                                if ($data.certificate.issuer) {
                                  _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                    default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                      if (_push7) {
                                        _push7(ssrRenderComponent(VTextField, mergeProps({
                                          modelValue: $data.certificate.issuer,
                                          "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                          disabled: "",
                                          placeholder: "Emissora",
                                          label: "Emissora"
                                        }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.issuer)), null, _parent7, _scopeId6));
                                      } else {
                                        return [
                                          withDirectives(createVNode(VTextField, {
                                            modelValue: $data.certificate.issuer,
                                            "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                            disabled: "",
                                            placeholder: "Emissora",
                                            label: "Emissora"
                                          }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                            [_directive_value, $data.certificate.issuer]
                                          ])
                                        ];
                                      }
                                    }),
                                    _: 1
                                  }, _parent6, _scopeId5));
                                } else {
                                  _push6(`<!---->`);
                                }
                                if ($data.certificate.status_ssl) {
                                  _push6(ssrRenderComponent(VCol, { cols: "12" }, {
                                    default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                      if (_push7) {
                                        _push7(ssrRenderComponent(VTextField, mergeProps({
                                          modelValue: $data.certificate.status_ssl,
                                          "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                          disabled: "",
                                          placeholder: "Status",
                                          label: "Status"
                                        }, ssrGetDirectiveProps(_ctx, _directive_value, $data.certificate.status_ssl)), null, _parent7, _scopeId6));
                                      } else {
                                        return [
                                          withDirectives(createVNode(VTextField, {
                                            modelValue: $data.certificate.status_ssl,
                                            "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                            disabled: "",
                                            placeholder: "Status",
                                            label: "Status"
                                          }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                            [_directive_value, $data.certificate.status_ssl]
                                          ])
                                        ];
                                      }
                                    }),
                                    _: 1
                                  }, _parent6, _scopeId5));
                                } else {
                                  _push6(`<!---->`);
                                }
                              } else {
                                return [
                                  $data.certificate.id ? (openBlock(), createBlock(VCol, {
                                    key: 0,
                                    cols: "12"
                                  }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.id,
                                        "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                        disabled: "",
                                        placeholder: "ID",
                                        label: "ID"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.id]
                                      ])
                                    ]),
                                    _: 1
                                  })) : createCommentVNode("", true),
                                  createVNode(VCol, { cols: "12" }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.domain,
                                        "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                        placeholder: "Dom\xEDnio",
                                        label: "Dom\xEDnio"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.domain]
                                      ])
                                    ]),
                                    _: 1
                                  }),
                                  createVNode(VCol, { cols: "12" }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.ssls_url,
                                        "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                        placeholder: "Url ssls",
                                        label: "Url ssls"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.ssls_url]
                                      ])
                                    ]),
                                    _: 1
                                  }),
                                  $data.certificate.activation_ssl ? (openBlock(), createBlock(VCol, {
                                    key: 1,
                                    cols: "12"
                                  }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.activation_ssl,
                                        "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                        disabled: "",
                                        placeholder: "Data da ativa\xE7\xE3o",
                                        label: "Data da ativa\xE7\xE3o"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.activation_ssl]
                                      ])
                                    ]),
                                    _: 1
                                  })) : createCommentVNode("", true),
                                  $data.certificate.expiration_ssl ? (openBlock(), createBlock(VCol, {
                                    key: 2,
                                    cols: "12"
                                  }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.expiration_ssl,
                                        "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                        disabled: "",
                                        placeholder: "Data expira\xE7\xE3o",
                                        label: "Data expira\xE7\xE3o"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.expiration_ssl]
                                      ])
                                    ]),
                                    _: 1
                                  })) : createCommentVNode("", true),
                                  $data.certificate.issuer ? (openBlock(), createBlock(VCol, {
                                    key: 3,
                                    cols: "12"
                                  }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.issuer,
                                        "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                        disabled: "",
                                        placeholder: "Emissora",
                                        label: "Emissora"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.issuer]
                                      ])
                                    ]),
                                    _: 1
                                  })) : createCommentVNode("", true),
                                  $data.certificate.status_ssl ? (openBlock(), createBlock(VCol, {
                                    key: 4,
                                    cols: "12"
                                  }, {
                                    default: withCtx(() => [
                                      withDirectives(createVNode(VTextField, {
                                        modelValue: $data.certificate.status_ssl,
                                        "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                        disabled: "",
                                        placeholder: "Status",
                                        label: "Status"
                                      }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                        [_directive_value, $data.certificate.status_ssl]
                                      ])
                                    ]),
                                    _: 1
                                  })) : createCommentVNode("", true)
                                ];
                              }
                            }),
                            _: 1
                          }, _parent5, _scopeId4));
                          _push5(ssrRenderComponent(VRow, null, {
                            default: withCtx((_5, _push6, _parent6, _scopeId5) => {
                              if (_push6) {
                                _push6(ssrRenderComponent(VCol, null, {
                                  default: withCtx((_6, _push7, _parent7, _scopeId6) => {
                                    if (_push7) {
                                      _push7(ssrRenderComponent(VBtn, {
                                        class: "mr-2",
                                        color: "error",
                                        outlined: "",
                                        to: "/ssl"
                                      }, {
                                        default: withCtx((_7, _push8, _parent8, _scopeId7) => {
                                          if (_push8) {
                                            _push8(` Cancelar `);
                                          } else {
                                            return [
                                              createTextVNode(" Cancelar ")
                                            ];
                                          }
                                        }),
                                        _: 1
                                      }, _parent7, _scopeId6));
                                      _push7(ssrRenderComponent(VBtn, {
                                        color: "success",
                                        outlined: "",
                                        onClick: $options.persistir
                                      }, {
                                        default: withCtx((_7, _push8, _parent8, _scopeId7) => {
                                          if (_push8) {
                                            _push8(` Salvar `);
                                          } else {
                                            return [
                                              createTextVNode(" Salvar ")
                                            ];
                                          }
                                        }),
                                        _: 1
                                      }, _parent7, _scopeId6));
                                    } else {
                                      return [
                                        createVNode(VBtn, {
                                          class: "mr-2",
                                          color: "error",
                                          outlined: "",
                                          to: "/ssl"
                                        }, {
                                          default: withCtx(() => [
                                            createTextVNode(" Cancelar ")
                                          ]),
                                          _: 1
                                        }),
                                        createVNode(VBtn, {
                                          color: "success",
                                          outlined: "",
                                          onClick: $options.persistir
                                        }, {
                                          default: withCtx(() => [
                                            createTextVNode(" Salvar ")
                                          ]),
                                          _: 1
                                        }, 8, ["onClick"])
                                      ];
                                    }
                                  }),
                                  _: 1
                                }, _parent6, _scopeId5));
                              } else {
                                return [
                                  createVNode(VCol, null, {
                                    default: withCtx(() => [
                                      createVNode(VBtn, {
                                        class: "mr-2",
                                        color: "error",
                                        outlined: "",
                                        to: "/ssl"
                                      }, {
                                        default: withCtx(() => [
                                          createTextVNode(" Cancelar ")
                                        ]),
                                        _: 1
                                      }),
                                      createVNode(VBtn, {
                                        color: "success",
                                        outlined: "",
                                        onClick: $options.persistir
                                      }, {
                                        default: withCtx(() => [
                                          createTextVNode(" Salvar ")
                                        ]),
                                        _: 1
                                      }, 8, ["onClick"])
                                    ]),
                                    _: 1
                                  })
                                ];
                              }
                            }),
                            _: 1
                          }, _parent5, _scopeId4));
                        } else {
                          return [
                            createVNode(VRow, { "no-gutters": "" }, {
                              default: withCtx(() => [
                                $data.certificate.id ? (openBlock(), createBlock(VCol, {
                                  key: 0,
                                  cols: "12"
                                }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.id,
                                      "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                      disabled: "",
                                      placeholder: "ID",
                                      label: "ID"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.id]
                                    ])
                                  ]),
                                  _: 1
                                })) : createCommentVNode("", true),
                                createVNode(VCol, { cols: "12" }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.domain,
                                      "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                      placeholder: "Dom\xEDnio",
                                      label: "Dom\xEDnio"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.domain]
                                    ])
                                  ]),
                                  _: 1
                                }),
                                createVNode(VCol, { cols: "12" }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.ssls_url,
                                      "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                      placeholder: "Url ssls",
                                      label: "Url ssls"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.ssls_url]
                                    ])
                                  ]),
                                  _: 1
                                }),
                                $data.certificate.activation_ssl ? (openBlock(), createBlock(VCol, {
                                  key: 1,
                                  cols: "12"
                                }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.activation_ssl,
                                      "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                      disabled: "",
                                      placeholder: "Data da ativa\xE7\xE3o",
                                      label: "Data da ativa\xE7\xE3o"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.activation_ssl]
                                    ])
                                  ]),
                                  _: 1
                                })) : createCommentVNode("", true),
                                $data.certificate.expiration_ssl ? (openBlock(), createBlock(VCol, {
                                  key: 2,
                                  cols: "12"
                                }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.expiration_ssl,
                                      "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                      disabled: "",
                                      placeholder: "Data expira\xE7\xE3o",
                                      label: "Data expira\xE7\xE3o"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.expiration_ssl]
                                    ])
                                  ]),
                                  _: 1
                                })) : createCommentVNode("", true),
                                $data.certificate.issuer ? (openBlock(), createBlock(VCol, {
                                  key: 3,
                                  cols: "12"
                                }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.issuer,
                                      "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                      disabled: "",
                                      placeholder: "Emissora",
                                      label: "Emissora"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.issuer]
                                    ])
                                  ]),
                                  _: 1
                                })) : createCommentVNode("", true),
                                $data.certificate.status_ssl ? (openBlock(), createBlock(VCol, {
                                  key: 4,
                                  cols: "12"
                                }, {
                                  default: withCtx(() => [
                                    withDirectives(createVNode(VTextField, {
                                      modelValue: $data.certificate.status_ssl,
                                      "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                      disabled: "",
                                      placeholder: "Status",
                                      label: "Status"
                                    }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                      [_directive_value, $data.certificate.status_ssl]
                                    ])
                                  ]),
                                  _: 1
                                })) : createCommentVNode("", true)
                              ]),
                              _: 1
                            }),
                            createVNode(VRow, null, {
                              default: withCtx(() => [
                                createVNode(VCol, null, {
                                  default: withCtx(() => [
                                    createVNode(VBtn, {
                                      class: "mr-2",
                                      color: "error",
                                      outlined: "",
                                      to: "/ssl"
                                    }, {
                                      default: withCtx(() => [
                                        createTextVNode(" Cancelar ")
                                      ]),
                                      _: 1
                                    }),
                                    createVNode(VBtn, {
                                      color: "success",
                                      outlined: "",
                                      onClick: $options.persistir
                                    }, {
                                      default: withCtx(() => [
                                        createTextVNode(" Salvar ")
                                      ]),
                                      _: 1
                                    }, 8, ["onClick"])
                                  ]),
                                  _: 1
                                })
                              ]),
                              _: 1
                            })
                          ];
                        }
                      }),
                      _: 1
                    }, _parent4, _scopeId3));
                  } else {
                    return [
                      createVNode(VForm, {
                        modelValue: _ctx.valid,
                        "onUpdate:modelValue": ($event) => _ctx.valid = $event
                      }, {
                        default: withCtx(() => [
                          createVNode(VRow, { "no-gutters": "" }, {
                            default: withCtx(() => [
                              $data.certificate.id ? (openBlock(), createBlock(VCol, {
                                key: 0,
                                cols: "12"
                              }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.id,
                                    "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                    disabled: "",
                                    placeholder: "ID",
                                    label: "ID"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.id]
                                  ])
                                ]),
                                _: 1
                              })) : createCommentVNode("", true),
                              createVNode(VCol, { cols: "12" }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.domain,
                                    "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                    placeholder: "Dom\xEDnio",
                                    label: "Dom\xEDnio"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.domain]
                                  ])
                                ]),
                                _: 1
                              }),
                              createVNode(VCol, { cols: "12" }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.ssls_url,
                                    "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                    placeholder: "Url ssls",
                                    label: "Url ssls"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.ssls_url]
                                  ])
                                ]),
                                _: 1
                              }),
                              $data.certificate.activation_ssl ? (openBlock(), createBlock(VCol, {
                                key: 1,
                                cols: "12"
                              }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.activation_ssl,
                                    "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                    disabled: "",
                                    placeholder: "Data da ativa\xE7\xE3o",
                                    label: "Data da ativa\xE7\xE3o"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.activation_ssl]
                                  ])
                                ]),
                                _: 1
                              })) : createCommentVNode("", true),
                              $data.certificate.expiration_ssl ? (openBlock(), createBlock(VCol, {
                                key: 2,
                                cols: "12"
                              }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.expiration_ssl,
                                    "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                    disabled: "",
                                    placeholder: "Data expira\xE7\xE3o",
                                    label: "Data expira\xE7\xE3o"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.expiration_ssl]
                                  ])
                                ]),
                                _: 1
                              })) : createCommentVNode("", true),
                              $data.certificate.issuer ? (openBlock(), createBlock(VCol, {
                                key: 3,
                                cols: "12"
                              }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.issuer,
                                    "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                    disabled: "",
                                    placeholder: "Emissora",
                                    label: "Emissora"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.issuer]
                                  ])
                                ]),
                                _: 1
                              })) : createCommentVNode("", true),
                              $data.certificate.status_ssl ? (openBlock(), createBlock(VCol, {
                                key: 4,
                                cols: "12"
                              }, {
                                default: withCtx(() => [
                                  withDirectives(createVNode(VTextField, {
                                    modelValue: $data.certificate.status_ssl,
                                    "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                    disabled: "",
                                    placeholder: "Status",
                                    label: "Status"
                                  }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                    [_directive_value, $data.certificate.status_ssl]
                                  ])
                                ]),
                                _: 1
                              })) : createCommentVNode("", true)
                            ]),
                            _: 1
                          }),
                          createVNode(VRow, null, {
                            default: withCtx(() => [
                              createVNode(VCol, null, {
                                default: withCtx(() => [
                                  createVNode(VBtn, {
                                    class: "mr-2",
                                    color: "error",
                                    outlined: "",
                                    to: "/ssl"
                                  }, {
                                    default: withCtx(() => [
                                      createTextVNode(" Cancelar ")
                                    ]),
                                    _: 1
                                  }),
                                  createVNode(VBtn, {
                                    color: "success",
                                    outlined: "",
                                    onClick: $options.persistir
                                  }, {
                                    default: withCtx(() => [
                                      createTextVNode(" Salvar ")
                                    ]),
                                    _: 1
                                  }, 8, ["onClick"])
                                ]),
                                _: 1
                              })
                            ]),
                            _: 1
                          })
                        ]),
                        _: 1
                      }, 8, ["modelValue", "onUpdate:modelValue"])
                    ];
                  }
                }),
                _: 1
              }, _parent3, _scopeId2));
            } else {
              return [
                createVNode(VCol, { cols: "6" }, {
                  default: withCtx(() => [
                    !$data.certificate.id ? (openBlock(), createBlock("h1", {
                      key: 0,
                      class: "text-center pb-5"
                    }, "Cadastro de certificados")) : createCommentVNode("", true),
                    $data.certificate.id ? (openBlock(), createBlock("h1", {
                      key: 1,
                      class: "text-center pb-5"
                    }, "Edi\xE7\xE3o de certificados")) : createCommentVNode("", true)
                  ]),
                  _: 1
                }),
                createVNode(VCol, { cols: "8" }, {
                  default: withCtx(() => [
                    createVNode(VForm, {
                      modelValue: _ctx.valid,
                      "onUpdate:modelValue": ($event) => _ctx.valid = $event
                    }, {
                      default: withCtx(() => [
                        createVNode(VRow, { "no-gutters": "" }, {
                          default: withCtx(() => [
                            $data.certificate.id ? (openBlock(), createBlock(VCol, {
                              key: 0,
                              cols: "12"
                            }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.id,
                                  "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                  disabled: "",
                                  placeholder: "ID",
                                  label: "ID"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.id]
                                ])
                              ]),
                              _: 1
                            })) : createCommentVNode("", true),
                            createVNode(VCol, { cols: "12" }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.domain,
                                  "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                  placeholder: "Dom\xEDnio",
                                  label: "Dom\xEDnio"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.domain]
                                ])
                              ]),
                              _: 1
                            }),
                            createVNode(VCol, { cols: "12" }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.ssls_url,
                                  "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                  placeholder: "Url ssls",
                                  label: "Url ssls"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.ssls_url]
                                ])
                              ]),
                              _: 1
                            }),
                            $data.certificate.activation_ssl ? (openBlock(), createBlock(VCol, {
                              key: 1,
                              cols: "12"
                            }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.activation_ssl,
                                  "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                  disabled: "",
                                  placeholder: "Data da ativa\xE7\xE3o",
                                  label: "Data da ativa\xE7\xE3o"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.activation_ssl]
                                ])
                              ]),
                              _: 1
                            })) : createCommentVNode("", true),
                            $data.certificate.expiration_ssl ? (openBlock(), createBlock(VCol, {
                              key: 2,
                              cols: "12"
                            }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.expiration_ssl,
                                  "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                  disabled: "",
                                  placeholder: "Data expira\xE7\xE3o",
                                  label: "Data expira\xE7\xE3o"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.expiration_ssl]
                                ])
                              ]),
                              _: 1
                            })) : createCommentVNode("", true),
                            $data.certificate.issuer ? (openBlock(), createBlock(VCol, {
                              key: 3,
                              cols: "12"
                            }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.issuer,
                                  "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                  disabled: "",
                                  placeholder: "Emissora",
                                  label: "Emissora"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.issuer]
                                ])
                              ]),
                              _: 1
                            })) : createCommentVNode("", true),
                            $data.certificate.status_ssl ? (openBlock(), createBlock(VCol, {
                              key: 4,
                              cols: "12"
                            }, {
                              default: withCtx(() => [
                                withDirectives(createVNode(VTextField, {
                                  modelValue: $data.certificate.status_ssl,
                                  "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                  disabled: "",
                                  placeholder: "Status",
                                  label: "Status"
                                }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                  [_directive_value, $data.certificate.status_ssl]
                                ])
                              ]),
                              _: 1
                            })) : createCommentVNode("", true)
                          ]),
                          _: 1
                        }),
                        createVNode(VRow, null, {
                          default: withCtx(() => [
                            createVNode(VCol, null, {
                              default: withCtx(() => [
                                createVNode(VBtn, {
                                  class: "mr-2",
                                  color: "error",
                                  outlined: "",
                                  to: "/ssl"
                                }, {
                                  default: withCtx(() => [
                                    createTextVNode(" Cancelar ")
                                  ]),
                                  _: 1
                                }),
                                createVNode(VBtn, {
                                  color: "success",
                                  outlined: "",
                                  onClick: $options.persistir
                                }, {
                                  default: withCtx(() => [
                                    createTextVNode(" Salvar ")
                                  ]),
                                  _: 1
                                }, 8, ["onClick"])
                              ]),
                              _: 1
                            })
                          ]),
                          _: 1
                        })
                      ]),
                      _: 1
                    }, 8, ["modelValue", "onUpdate:modelValue"])
                  ]),
                  _: 1
                })
              ];
            }
          }),
          _: 1
        }, _parent2, _scopeId));
      } else {
        return [
          createVNode(VRow, {
            "no-gutters": "",
            class: "py-10 justify-center"
          }, {
            default: withCtx(() => [
              createVNode(VCol, { cols: "6" }, {
                default: withCtx(() => [
                  !$data.certificate.id ? (openBlock(), createBlock("h1", {
                    key: 0,
                    class: "text-center pb-5"
                  }, "Cadastro de certificados")) : createCommentVNode("", true),
                  $data.certificate.id ? (openBlock(), createBlock("h1", {
                    key: 1,
                    class: "text-center pb-5"
                  }, "Edi\xE7\xE3o de certificados")) : createCommentVNode("", true)
                ]),
                _: 1
              }),
              createVNode(VCol, { cols: "8" }, {
                default: withCtx(() => [
                  createVNode(VForm, {
                    modelValue: _ctx.valid,
                    "onUpdate:modelValue": ($event) => _ctx.valid = $event
                  }, {
                    default: withCtx(() => [
                      createVNode(VRow, { "no-gutters": "" }, {
                        default: withCtx(() => [
                          $data.certificate.id ? (openBlock(), createBlock(VCol, {
                            key: 0,
                            cols: "12"
                          }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.id,
                                "onUpdate:modelValue": ($event) => $data.certificate.id = $event,
                                disabled: "",
                                placeholder: "ID",
                                label: "ID"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.id]
                              ])
                            ]),
                            _: 1
                          })) : createCommentVNode("", true),
                          createVNode(VCol, { cols: "12" }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.domain,
                                "onUpdate:modelValue": ($event) => $data.certificate.domain = $event,
                                placeholder: "Dom\xEDnio",
                                label: "Dom\xEDnio"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.domain]
                              ])
                            ]),
                            _: 1
                          }),
                          createVNode(VCol, { cols: "12" }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.ssls_url,
                                "onUpdate:modelValue": ($event) => $data.certificate.ssls_url = $event,
                                placeholder: "Url ssls",
                                label: "Url ssls"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.ssls_url]
                              ])
                            ]),
                            _: 1
                          }),
                          $data.certificate.activation_ssl ? (openBlock(), createBlock(VCol, {
                            key: 1,
                            cols: "12"
                          }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.activation_ssl,
                                "onUpdate:modelValue": ($event) => $data.certificate.activation_ssl = $event,
                                disabled: "",
                                placeholder: "Data da ativa\xE7\xE3o",
                                label: "Data da ativa\xE7\xE3o"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.activation_ssl]
                              ])
                            ]),
                            _: 1
                          })) : createCommentVNode("", true),
                          $data.certificate.expiration_ssl ? (openBlock(), createBlock(VCol, {
                            key: 2,
                            cols: "12"
                          }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.expiration_ssl,
                                "onUpdate:modelValue": ($event) => $data.certificate.expiration_ssl = $event,
                                disabled: "",
                                placeholder: "Data expira\xE7\xE3o",
                                label: "Data expira\xE7\xE3o"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.expiration_ssl]
                              ])
                            ]),
                            _: 1
                          })) : createCommentVNode("", true),
                          $data.certificate.issuer ? (openBlock(), createBlock(VCol, {
                            key: 3,
                            cols: "12"
                          }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.issuer,
                                "onUpdate:modelValue": ($event) => $data.certificate.issuer = $event,
                                disabled: "",
                                placeholder: "Emissora",
                                label: "Emissora"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.issuer]
                              ])
                            ]),
                            _: 1
                          })) : createCommentVNode("", true),
                          $data.certificate.status_ssl ? (openBlock(), createBlock(VCol, {
                            key: 4,
                            cols: "12"
                          }, {
                            default: withCtx(() => [
                              withDirectives(createVNode(VTextField, {
                                modelValue: $data.certificate.status_ssl,
                                "onUpdate:modelValue": ($event) => $data.certificate.status_ssl = $event,
                                disabled: "",
                                placeholder: "Status",
                                label: "Status"
                              }, null, 8, ["modelValue", "onUpdate:modelValue"]), [
                                [_directive_value, $data.certificate.status_ssl]
                              ])
                            ]),
                            _: 1
                          })) : createCommentVNode("", true)
                        ]),
                        _: 1
                      }),
                      createVNode(VRow, null, {
                        default: withCtx(() => [
                          createVNode(VCol, null, {
                            default: withCtx(() => [
                              createVNode(VBtn, {
                                class: "mr-2",
                                color: "error",
                                outlined: "",
                                to: "/ssl"
                              }, {
                                default: withCtx(() => [
                                  createTextVNode(" Cancelar ")
                                ]),
                                _: 1
                              }),
                              createVNode(VBtn, {
                                color: "success",
                                outlined: "",
                                onClick: $options.persistir
                              }, {
                                default: withCtx(() => [
                                  createTextVNode(" Salvar ")
                                ]),
                                _: 1
                              }, 8, ["onClick"])
                            ]),
                            _: 1
                          })
                        ]),
                        _: 1
                      })
                    ]),
                    _: 1
                  }, 8, ["modelValue", "onUpdate:modelValue"])
                ]),
                _: 1
              })
            ]),
            _: 1
          })
        ];
      }
    }),
    _: 1
  }, _parent));
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/ssl/[id].vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const _id_ = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);

export { _id_ as default };
//# sourceMappingURL=_id_-063ad2c2.mjs.map
