process coverage {
    tag "$sample_id"
    container 'quay.io/biocontainers/mosdepth:0.3.3--hdfd78af_1'
    publishDir "${params.outdir}/$sample_id/coverage/", mode: 'copy'


    input:
    tuple val(sample_id),  path(bam), path(bai)
    path(bed)

    output:
    tuple val(sample_id), path('*.global.dist.txt')      , emit: global_txt
    tuple val(sample_id), path('*.summary.txt')          , emit: summary_txt
    tuple val(sample_id), path('*.region.dist.txt')      , optional:true, emit: regions_txt
    tuple val(sample_id), path('*.per-base.d4')          , optional:true, emit: per_base_d4
    tuple val(sample_id), path('*.per-base.bed.gz')      , optional:true, emit: per_base_bed
    tuple val(sample_id), path('*.per-base.bed.gz.csi')  , optional:true, emit: per_base_csi
    tuple val(sample_id), path('*.regions.bed.gz')       , optional:true, emit: regions_bed
    tuple val(sample_id), path('*.regions.bed.gz.csi')   , optional:true, emit: regions_csi
    tuple val(sample_id), path('*.quantized.bed.gz')     , optional:true, emit: quantized_bed
    tuple val(sample_id), path('*.quantized.bed.gz.csi') , optional:true, emit: quantized_csi
    tuple val(sample_id), path('*.thresholds.bed.gz')    , optional:true, emit: thresholds_bed
    tuple val(sample_id), path('*.thresholds.bed.gz.csi'), optional:true, emit: thresholds_csi
    path  "versions.yml"                            , emit: versions

    script:

    """
    mosdepth \\
        --threads $task.cpus \\
        --by ${bed} \\
        $sample_id \\
        $bam

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        mosdepth: \$(mosdepth --version 2>&1 | sed 's/^.*mosdepth //; s/ .*\$//')
    END_VERSIONS
    """
}