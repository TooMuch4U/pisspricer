<template>
  <div :id="modalId" class="modal fade" role="dialog" tabindex="-1">
    <div class="modal-dialog modal-xl" role="document">
      <div class="modal-content">

        <!-- Title section of modal -->
        <div class="modal-header">
          <h5 class="modal-title">{{ modalHeader }}</h5>
          <button aria-label="Close" class="close" data-dismiss="modal" type="button">
            <span ref="close" aria-hidden="true">&times;</span>
          </button>
        </div>

        <!-- Body section of modal -->
        <div class="modal-body overflow-scroll">
          <slot/>
        </div>

        <!-- Footer / button section of modal -->
        <div class="modal-footer">
          <button class="btn btn-secondary" data-dismiss="modal" type="button">
            {{ modalDismissText }}
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BasicModal',
  props: {
    modalId: String,
    modalHeader: String,
    modalDismissText: String
  }
}
</script>
