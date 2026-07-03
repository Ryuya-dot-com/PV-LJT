#!/usr/bin/env python3
"""Create v6 candidate PV-LJT materials after the critical design audit.

This script intentionally does not create audio recording scripts. The output is
a pre-audio candidate pool and expert-review packet.
"""

from __future__ import annotations

import csv
import random
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "materials"

ITEMS_V5 = MATERIALS / "aural_pv_ljt_items_v5_production.tsv"
V6_FEASIBILITY = MATERIALS / "ljt_v6_item_feasibility_audit_v1.tsv"

ITEMS_V6 = MATERIALS / "aural_pv_ljt_items_v6_candidate.tsv"
ASSIGNMENT_V6 = MATERIALS / "aural_pv_ljt_list_assignment_v6_candidate.tsv"
LIST_A_V6 = MATERIALS / "aural_pv_ljt_list_A_v6_candidate.tsv"
LIST_B_V6 = MATERIALS / "aural_pv_ljt_list_B_v6_candidate.tsv"
REVIEW_FORM_V6 = MATERIALS / "ljt_v6_candidate_expert_review_form_v1.tsv"
PRE_AUDIO_AUDIT_V6 = MATERIALS / "ljt_v6_candidate_pre_audio_audit_v1.tsv"
RED_TEAM_V6 = MATERIALS / "ljt_v6_candidate_red_team_review_v1.tsv"
EXCLUDED_TARGETS_V6 = MATERIALS / "ljt_v6_excluded_targets_v1.tsv"
SUMMARY_V6 = MATERIALS / "ljt_v6_candidate_design_summary_v1.md"

SEED = 20260703


# Pair-level ratings are conservative internal ratings, not native-speaker
# validation. 1 = weak/high risk, 4 = strong/low risk depending on the field.
CANDIDATE_PAIRS: dict[str, dict[str, str]] = {
    "pv_001": {
        "acceptable": "The union broke off the talks.",
        "unacceptable": "The union broke off the proposal.",
        "mismatch_type": "same_domain_collocation_mismatch",
        "pair_rationale": "Both objects belong to negotiation contexts; the unacceptable item targets the fact that break off selects talks or relations, not a proposal itself.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_002": {
        "acceptable": "The guard handed over the prisoner.",
        "unacceptable": "The guard handed over the arrest.",
        "mismatch_type": "same_domain_object_mismatch",
        "pair_rationale": "Both objects are legal-domain nouns; the unacceptable item keeps the domain but uses an event noun that cannot be handed over as custody or control.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_008": {
        "acceptable": "The team moved up to first place.",
        "unacceptable": "The team moved up to last place.",
        "mismatch_type": "directional_hierarchy_mismatch",
        "pair_rationale": "Both outcomes are ranking positions; rejection depends on knowing that move up denotes upward rank movement.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "4",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_009": {
        "acceptable": "The passengers got on the train.",
        "unacceptable": "The passengers got on the station.",
        "mismatch_type": "transport_anchor_mismatch",
        "pair_rationale": "Both nouns are transport-domain nouns; only a vehicle-like noun is compatible with the boarding sense.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_011": {
        "acceptable": "One essay stood out among submissions.",
        "unacceptable": "One essay stood out among pages.",
        "mismatch_type": "comparison_set_mismatch",
        "pair_rationale": "Both nouns are writing-domain nouns; the unacceptable item changes the comparison set from same-class submissions to document parts.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_012": {
        "acceptable": "Investors pulled back from the project.",
        "unacceptable": "Investors pulled back from the approval.",
        "mismatch_type": "same_domain_complement_mismatch",
        "pair_rationale": "Both complements are decision-domain nouns; the unacceptable item uses a state/result where an activity or commitment is expected.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_013": {
        "acceptable": "The lab ran out of samples.",
        "unacceptable": "The lab ran out of findings.",
        "mismatch_type": "resource_depletion_mismatch",
        "pair_rationale": "Both objects are research-domain nouns; samples can be depleted as supplies, whereas findings are not normally used up as a stock.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_014": {
        "acceptable": "The clerk turned over the records to police.",
        "unacceptable": "The clerk turned over the permission to police.",
        "mismatch_type": "authority_transfer_object_mismatch",
        "pair_rationale": "Both objects are administrative/legal nouns; records can be surrendered to authorities, but permission is not an object surrendered in this frame.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_015": {
        "acceptable": "The theater put on a musical.",
        "unacceptable": "The theater put on a ticket.",
        "mismatch_type": "event_staging_object_mismatch",
        "pair_rationale": "Both objects belong to theater contexts; the unacceptable item uses a theater-related artifact rather than an event or performance.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_016": {
        "acceptable": "The team took back the lead.",
        "unacceptable": "The team took back the loss.",
        "mismatch_type": "regain_control_object_mismatch",
        "pair_rationale": "Both nouns are sports-outcome nouns; lead can be regained, whereas loss is not normally regained by taking it back.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_018": {
        "acceptable": "The investment paid off quickly.",
        "unacceptable": "The invoice paid off quickly.",
        "mismatch_type": "finance_domain_subject_mismatch",
        "pair_rationale": "Both subjects are finance-domain nouns; investment can yield a benefit, while invoice is not normally an intransitive source of payoff.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_019": {
        "acceptable": "The passengers got off the ferry.",
        "unacceptable": "The passengers got off the terminal.",
        "mismatch_type": "transport_anchor_mismatch",
        "pair_rationale": "Both nouns are transport-domain nouns; only the vehicle-like noun supports the leave-a-vehicle sense.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_020": {
        "acceptable": "The witness turned up at court.",
        "unacceptable": "The witness turned up at testimony.",
        "mismatch_type": "appearance_location_mismatch",
        "pair_rationale": "Both complements are legal-domain nouns; court is a location/event site, whereas testimony is not a place where someone turns up.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_022": {
        "acceptable": "The host cut off the caller abruptly.",
        "unacceptable": "The host cut off the topic abruptly.",
        "mismatch_type": "interaction_participant_mismatch",
        "pair_rationale": "Both objects belong to talk-show discourse; the target sense selects an active speaker, not the topic of conversation.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "3",
    },
    "pv_023": {
        "acceptable": "The firm brought in a consultant.",
        "unacceptable": "The firm brought in a consultation.",
        "mismatch_type": "recruitment_role_mismatch",
        "pair_rationale": "Both objects are professional-service nouns; the target sense requires a person or role, not the service event itself.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_026": {
        "acceptable": "The report set out the procedure.",
        "unacceptable": "The report set out the appendix.",
        "mismatch_type": "document_content_mismatch",
        "pair_rationale": "Both nouns are document-domain nouns; the target sense selects an explanation or rules, not a document section as such.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_027": {
        "acceptable": "The coach broke down the play.",
        "unacceptable": "The coach broke down the whistle.",
        "mismatch_type": "analysis_object_mismatch",
        "pair_rationale": "Both nouns are sports-domain nouns; a play can be analyzed into parts, whereas a whistle is not an analytical problem in this frame.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_028": {
        "acceptable": "The nurse reached out to patients.",
        "unacceptable": "The nurse reached out to symptoms.",
        "mismatch_type": "recipient_mismatch",
        "pair_rationale": "Both complements are health-domain nouns; the target sense requires a person or group that can be contacted.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_030": {
        "acceptable": "The crew put up the banner.",
        "unacceptable": "The crew put up the brochure.",
        "mismatch_type": "display_attach_object_mismatch",
        "pair_rationale": "Both objects are display/publicity materials, but brochure remains too plausible in a posting context; keep as reserve pending native review.",
        "pool_status": "reserve_needs_native_review",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "2",
        "pv_dependency_1_4": "2",
        "general_cue_risk_1_4": "3",
        "alternate_sense_risk_1_4": "3",
    },
    "pv_031": {
        "acceptable": "The coach turned around the season.",
        "unacceptable": "The coach turned around the defeat.",
        "mismatch_type": "improvement_object_mismatch",
        "pair_rationale": "Both objects are sports-outcome nouns; a season can be transformed, whereas a defeat itself is not normally turned around after the fact.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_032": {
        "acceptable": "The data backed up the conclusion.",
        "unacceptable": "The data backed up the confusion.",
        "mismatch_type": "evidence_support_object_mismatch",
        "pair_rationale": "Both nouns are research-discourse nouns; data can support a conclusion, but not confusion as a claim.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_034": {
        "acceptable": "She took out a mortgage.",
        "unacceptable": "She took out a receipt.",
        "mismatch_type": "official_document_mismatch",
        "pair_rationale": "Both objects are finance/document nouns; mortgage fits the obtain-an-official-service sense, while receipt does not.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_040": {
        "acceptable": "The secret came out during trial.",
        "unacceptable": "The witness came out during trial.",
        "mismatch_type": "revelation_subject_mismatch",
        "pair_rationale": "Both subjects are legal-domain nouns; the acceptable subject is hidden information, whereas the unacceptable subject is a person and risks alternate literal readings.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "3",
    },
    "pv_041": {
        "acceptable": "The reforms brought about change.",
        "unacceptable": "The reforms brought about evidence.",
        "mismatch_type": "causal_result_mismatch",
        "pair_rationale": "Both objects are policy/research nouns; reforms can cause change, whereas evidence is normally produced or found rather than brought about by reforms.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_042": {
        "acceptable": "The researchers carried out the analysis.",
        "unacceptable": "The researchers carried out the hypothesis.",
        "mismatch_type": "research_task_mismatch",
        "pair_rationale": "Both objects are research-domain nouns; analysis is a task that can be carried out, whereas hypothesis is a proposition to test.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "4",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_043": {
        "acceptable": "The doctor ruled out infection.",
        "unacceptable": "The doctor ruled out symptoms.",
        "mismatch_type": "diagnostic_possibility_mismatch",
        "pair_rationale": "Both objects are medical-domain nouns; infection can be excluded as a possibility, whereas symptoms are observed signs, not the ruled-out condition.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "4",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_044": {
        "acceptable": "The review pointed out the limitation.",
        "unacceptable": "The review pointed out the appendix.",
        "mismatch_type": "information_object_mismatch",
        "pair_rationale": "Both objects are academic-document nouns; the review can identify a limitation, whereas appendix is a document part and creates weaker target fit.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "2",
    },
    "pv_045": {
        "acceptable": "The abstract summed up the study.",
        "unacceptable": "The abstract summed up the heading.",
        "mismatch_type": "summary_object_mismatch",
        "pair_rationale": "Both nouns are academic-document nouns; an abstract summarizes a study, not a heading.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "4",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_046": {
        "acceptable": "The doctor followed up after the treatment.",
        "unacceptable": "The doctor followed up after the thermometer.",
        "mismatch_type": "follow_up_event_mismatch",
        "pair_rationale": "Both complements are medical-domain nouns; the follow-up frame requires an event or case, not an instrument.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_047": {
        "acceptable": "The diagram laid out the process.",
        "unacceptable": "The diagram laid out the footnote.",
        "mismatch_type": "information_organization_mismatch",
        "pair_rationale": "Both objects are document/information nouns; diagram can present a process clearly, not normally a footnote.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "4",
        "pv_dependency_1_4": "4",
        "general_cue_risk_1_4": "1",
        "alternate_sense_risk_1_4": "1",
    },
    "pv_048": {
        "acceptable": "The students worked out the equation.",
        "unacceptable": "The students worked out the pencil.",
        "mismatch_type": "problem_solving_object_mismatch",
        "pair_rationale": "Both objects are classroom-domain nouns; equation is a problem that can be solved, whereas pencil is not.",
        "pool_status": "active_candidate",
        "acceptable_naturalness_1_4": "4",
        "unacceptable_near_miss_1_4": "3",
        "pv_dependency_1_4": "3",
        "general_cue_risk_1_4": "2",
        "alternate_sense_risk_1_4": "1",
    },
}


RED_TEAM_NOTES: dict[str, dict[str, str]] = {
    "pv_001": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "collocation_vs_construct",
        "red_team_note": "Proposal is same-domain, but rejection may still reduce to collocation knowledge rather than the full end-talks sense.",
    },
    "pv_002": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "event_noun_cue",
        "red_team_note": "Arrest is a legal-domain event noun; participants may reject from noun type rather than transfer-of-control meaning.",
    },
    "pv_008": {
        "red_team_risk_level": "low",
        "residual_risk_type": "minimal",
        "red_team_note": "Rank direction is locally tied to the particle meaning and is comparatively robust.",
    },
    "pv_009": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "transport_world_knowledge",
        "red_team_note": "Station is same-domain, but vehicle vs place knowledge may make the item easier than intended.",
    },
    "pv_011": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "comparison_class_cue",
        "red_team_note": "Pages are document-domain but not same-class alternatives; rejection may come from comparison-set oddness.",
    },
    "pv_012": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "abstract_complement_cue",
        "red_team_note": "Approval is decision-domain, but the item may still be rejected because it is not an activity or commitment.",
    },
    "pv_013": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "depletion_world_knowledge",
        "red_team_note": "Findings are same research domain, but the depleted-resource contrast remains fairly transparent.",
    },
    "pv_014": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "transfer_object_cue",
        "red_team_note": "Permission is administrative but may be rejected from object transferability rather than PV knowledge.",
    },
    "pv_015": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "object_category_cue",
        "red_team_note": "Ticket is theater-domain, but event vs artifact remains a broad cue.",
    },
    "pv_016": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "sports_outcome_cue",
        "red_team_note": "Lead/loss is same-domain, but the direction of regain may be recoverable from sports semantics.",
    },
    "pv_018": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "finance_subject_cue",
        "red_team_note": "Invoice is finance-domain, but participants may reject it because it is not an agentive investment or effort.",
    },
    "pv_019": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "transport_world_knowledge",
        "red_team_note": "Terminal is same-domain, but vehicle vs place knowledge may make the item easier than intended.",
    },
    "pv_020": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "location_complement_cue",
        "red_team_note": "Testimony is legal-domain, but the place/event-site contrast remains a general cue.",
    },
    "pv_022": {
        "red_team_risk_level": "high",
        "residual_risk_type": "alternate_sense_risk",
        "red_team_note": "Cut off the topic may be interpretable as ending discussion of a topic; revise before audio.",
    },
    "pv_023": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "human_role_cue",
        "red_team_note": "Consultant/consultation controls domain but still creates a person-vs-event cue.",
    },
    "pv_026": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "possible_document_reading",
        "red_team_note": "A report could arguably set out an appendix in a document-organization sense; native review should check acceptability.",
    },
    "pv_027": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "analysis_object_cue",
        "red_team_note": "Whistle is sports-domain, but rejection may come from broad analyzability.",
    },
    "pv_028": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "recipient_animacy_cue",
        "red_team_note": "Patients/symptoms controls domain but retains an animacy/recipient cue.",
    },
    "pv_030": {
        "red_team_risk_level": "high",
        "residual_risk_type": "plausible_alternate_context",
        "red_team_note": "Brochure can be put up in some display contexts; keep as reserve, not active list.",
    },
    "pv_031": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "sports_outcome_cue",
        "red_team_note": "Defeat is same-domain, but rejection may be recoverable from outcome semantics.",
    },
    "pv_032": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "claim_object_cue",
        "red_team_note": "Confusion is research-discourse related, but it is not a claim; cue remains broad.",
    },
    "pv_034": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "official_document_cue",
        "red_team_note": "Receipt is finance/document-domain but the official-service contrast is still transparent.",
    },
    "pv_040": {
        "red_team_risk_level": "high",
        "residual_risk_type": "alternate_sense_risk",
        "red_team_note": "Witness came out can have literal or identity-disclosure readings; revise before audio.",
    },
    "pv_041": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "result_object_cue",
        "red_team_note": "Evidence is policy/research-domain but may be rejected because it is not an event/result caused by reforms.",
    },
    "pv_042": {
        "red_team_risk_level": "low",
        "residual_risk_type": "minimal",
        "red_team_note": "Analysis/hypothesis is a strong task-vs-proposition contrast within research discourse.",
    },
    "pv_043": {
        "red_team_risk_level": "low",
        "residual_risk_type": "minimal",
        "red_team_note": "Condition-vs-symptom contrast is medically local and stable for the exclude-possibility sense.",
    },
    "pv_044": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "possible_document_reading",
        "red_team_note": "A review can point out an appendix in some contexts; native review should test whether it is truly unacceptable.",
    },
    "pv_045": {
        "red_team_risk_level": "low",
        "residual_risk_type": "minimal",
        "red_team_note": "Study/heading contrast is local to summarization and comparatively stable.",
    },
    "pv_046": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "event_vs_instrument_cue",
        "red_team_note": "Treatment/thermometer controls medical domain, but event-vs-instrument cue remains salient.",
    },
    "pv_047": {
        "red_team_risk_level": "low",
        "residual_risk_type": "minimal",
        "red_team_note": "Process/footnote contrast is local to information organization and comparatively stable.",
    },
    "pv_048": {
        "red_team_risk_level": "moderate",
        "residual_risk_type": "problem_object_cue",
        "red_team_note": "Equation/pencil controls classroom domain, but problem-vs-tool cue remains broad.",
    },
}


CUE_PATTERN = re.compile(
    r"\b(but|although|however|yet|nevertheless|never|no|none|nothing|without|despite)\b",
    re.IGNORECASE,
)
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def word_count(text: str) -> int:
    return len(WORD_PATTERN.findall(text))


def has_cue(text: str) -> bool:
    return bool(CUE_PATTERN.search(text))


def load_inputs() -> tuple[dict[tuple[str, str], dict[str, str]], dict[str, dict[str, str]]]:
    item_rows, _ = read_tsv(ITEMS_V5)
    feasibility_rows, _ = read_tsv(V6_FEASIBILITY)
    by_pair = {(row["pv_id"], row["condition"]): row for row in item_rows}
    feasibility = {row["pv_id"]: row for row in feasibility_rows}
    return by_pair, feasibility


def target_form_in_both(acceptable: str, unacceptable: str, target_form: str) -> bool:
    target = target_form.lower()
    return target in acceptable.lower() and target in unacceptable.lower()


def gate_status(spec: dict[str, str], target_ok: bool, a_wc: int, u_wc: int) -> str:
    if spec["pool_status"] != "active_candidate":
        return "reserve_not_listed"
    if (
        int(spec["acceptable_naturalness_1_4"]) >= 3
        and int(spec["unacceptable_near_miss_1_4"]) >= 3
        and int(spec["pv_dependency_1_4"]) >= 3
        and int(spec["general_cue_risk_1_4"]) <= 2
        and int(spec["alternate_sense_risk_1_4"]) <= 2
        and abs(u_wc - a_wc) <= 1
        and target_ok
        and not has_cue(spec["acceptable"])
        and not has_cue(spec["unacceptable"])
    ):
        return "prelim_pass_native_review_required"
    return "prelim_review_required"


def make_items() -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    by_pair, feasibility = load_inputs()
    rows: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []

    item_fields = [
        "ljt_item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "target_form",
        "sentence_text",
        "intended_sense",
        "mismatch_type",
        "source_material",
        "notes",
        "v6_pool_status",
        "candidate_gate_status",
        "pair_rationale",
    ]

    for pv_id in sorted(CANDIDATE_PAIRS):
        spec = CANDIDATE_PAIRS[pv_id]
        base_a = by_pair[(pv_id, "acceptable")]
        base_u = by_pair[(pv_id, "unacceptable")]
        target_form = base_a["target_form"]
        a_wc = word_count(spec["acceptable"])
        u_wc = word_count(spec["unacceptable"])
        target_ok = target_form_in_both(spec["acceptable"], spec["unacceptable"], target_form)
        status = gate_status(spec, target_ok, a_wc, u_wc)

        for condition, base, sentence, mismatch in [
            ("acceptable", base_a, spec["acceptable"], "none"),
            ("unacceptable", base_u, spec["unacceptable"], spec["mismatch_type"]),
        ]:
            rows.append(
                {
                    "ljt_item_id": base["ljt_item_id"],
                    "pv_id": pv_id,
                    "pv": base["pv"],
                    "condition": condition,
                    "expected_response": condition,
                    "target_form": base["target_form"],
                    "sentence_text": sentence,
                    "intended_sense": base["intended_sense"],
                    "mismatch_type": mismatch,
                    "source_material": base["source_material"],
                    "notes": "v6 candidate: pre-audio expert review required; do not record yet",
                    "v6_pool_status": spec["pool_status"],
                    "candidate_gate_status": status,
                    "pair_rationale": spec["pair_rationale"],
                }
            )

        audit_rows.append(
            {
                "pv_id": pv_id,
                "pv": base_a["pv"],
                "v6_action": feasibility[pv_id]["v6_action"],
                "v6_pool_status": spec["pool_status"],
                "candidate_gate_status": status,
                "acceptable_item_id": base_a["ljt_item_id"],
                "acceptable_sentence": spec["acceptable"],
                "unacceptable_item_id": base_u["ljt_item_id"],
                "unacceptable_sentence": spec["unacceptable"],
                "acceptable_word_count": str(a_wc),
                "unacceptable_word_count": str(u_wc),
                "word_count_delta_unacceptable_minus_acceptable": str(u_wc - a_wc),
                "acceptable_has_overt_cue": str(has_cue(spec["acceptable"])).lower(),
                "unacceptable_has_overt_cue": str(has_cue(spec["unacceptable"])).lower(),
                "target_form_in_both": str(target_ok).lower(),
                "acceptable_naturalness_1_4": spec["acceptable_naturalness_1_4"],
                "unacceptable_near_miss_1_4": spec["unacceptable_near_miss_1_4"],
                "pv_dependency_1_4": spec["pv_dependency_1_4"],
                "general_cue_risk_1_4": spec["general_cue_risk_1_4"],
                "alternate_sense_risk_1_4": spec["alternate_sense_risk_1_4"],
                "pair_rationale": spec["pair_rationale"],
                "critical_note": feasibility[pv_id]["critical_note"],
            }
        )

    write_tsv(ITEMS_V6, rows, item_fields)
    return rows, audit_rows, item_fields


def make_review_form(items: list[dict[str, str]], audit_rows: list[dict[str, str]]) -> None:
    audit_by_pv = {row["pv_id"]: row for row in audit_rows}
    fields = [
        "ljt_item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "sentence_text",
        "target_form",
        "intended_sense",
        "mismatch_type",
        "word_count",
        "has_overt_cue",
        "v6_pool_status",
        "candidate_gate_status",
        "acceptable_naturalness_1_4_candidate",
        "unacceptable_near_miss_1_4_candidate",
        "pv_dependency_1_4_candidate",
        "general_cue_risk_1_4_candidate",
        "alternate_sense_risk_1_4_candidate",
        "pair_rationale",
        "reviewer_naturalness_1_4",
        "reviewer_target_sense_fit_1_4",
        "reviewer_general_cue_risk_1_4",
        "reviewer_decision_keep_revise_drop",
        "reviewer_comment",
    ]
    rows = []
    for item in items:
        audit = audit_by_pv[item["pv_id"]]
        rows.append(
            {
                **item,
                "word_count": str(word_count(item["sentence_text"])),
                "has_overt_cue": str(has_cue(item["sentence_text"])).lower(),
                "acceptable_naturalness_1_4_candidate": audit["acceptable_naturalness_1_4"],
                "unacceptable_near_miss_1_4_candidate": audit["unacceptable_near_miss_1_4"],
                "pv_dependency_1_4_candidate": audit["pv_dependency_1_4"],
                "general_cue_risk_1_4_candidate": audit["general_cue_risk_1_4"],
                "alternate_sense_risk_1_4_candidate": audit["alternate_sense_risk_1_4"],
            }
        )
    write_tsv(REVIEW_FORM_V6, rows, fields)


def make_lists(items: list[dict[str, str]]) -> None:
    item_by_id = {row["ljt_item_id"]: row for row in items}
    active_pv_ids = [
        pv_id
        for pv_id, spec in sorted(CANDIDATE_PAIRS.items())
        if spec["pool_status"] == "active_candidate"
    ]
    if len(active_pv_ids) % 2 != 0:
        raise ValueError("Active PV count must be even for balanced list assignment.")

    assignment_fields = [
        "pv_id",
        "pv",
        "v6_pool_status",
        "candidate_gate_status",
        "list_A_item_id",
        "list_A_condition",
        "list_B_item_id",
        "list_B_condition",
        "pair_rationale",
    ]
    assignment_rows = []
    for index, pv_id in enumerate(active_pv_ids):
        a_condition = "acceptable" if index % 2 == 0 else "unacceptable"
        b_condition = "unacceptable" if a_condition == "acceptable" else "acceptable"
        item_a = next(row for row in items if row["pv_id"] == pv_id and row["condition"] == a_condition)
        item_b = next(row for row in items if row["pv_id"] == pv_id and row["condition"] == b_condition)
        assignment_rows.append(
            {
                "pv_id": pv_id,
                "pv": item_a["pv"],
                "v6_pool_status": item_a["v6_pool_status"],
                "candidate_gate_status": item_a["candidate_gate_status"],
                "list_A_item_id": item_a["ljt_item_id"],
                "list_A_condition": item_a["condition"],
                "list_B_item_id": item_b["ljt_item_id"],
                "list_B_condition": item_b["condition"],
                "pair_rationale": item_a["pair_rationale"],
            }
        )

    write_tsv(ASSIGNMENT_V6, assignment_rows, assignment_fields)

    list_fields = [
        "trial_order",
        "list_id",
        "ljt_item_id",
        "pv_id",
        "pv",
        "condition",
        "expected_response",
        "target_form",
        "sentence_text",
        "intended_sense",
        "mismatch_type",
        "source_material",
        "v6_pool_status",
        "candidate_gate_status",
        "pair_rationale",
        "notes",
    ]
    for list_id, list_key, out_path in [
        ("A", "list_A_item_id", LIST_A_V6),
        ("B", "list_B_item_id", LIST_B_V6),
    ]:
        rows = []
        ids = [row[list_key] for row in assignment_rows]
        rng = random.Random(SEED + (1 if list_id == "A" else 2))
        rng.shuffle(ids)
        for order, item_id in enumerate(ids, start=1):
            item = item_by_id[item_id]
            rows.append({"trial_order": str(order), "list_id": list_id, **item})
        write_tsv(out_path, rows, list_fields)


def make_excluded(feasibility: dict[str, dict[str, str]]) -> None:
    fields = [
        "pv_id",
        "pv",
        "source",
        "meaning",
        "register_focus",
        "v6_action",
        "construct_fit_1_4",
        "near_miss_feasibility_1_4",
        "polysemy_risk_1_4",
        "audio_risk_1_4",
        "replacement_priority",
        "critical_note",
    ]
    rows = []
    for pv_id, row in sorted(feasibility.items()):
        if pv_id in CANDIDATE_PAIRS:
            continue
        replacement_priority = "drop"
        if row["v6_action"] == "replace_or_rewrite":
            replacement_priority = "replace_before_audio"
        rows.append({**row, "replacement_priority": replacement_priority})
    write_tsv(EXCLUDED_TARGETS_V6, rows, fields)


def make_audit_and_summary(audit_rows: list[dict[str, str]], feasibility: dict[str, dict[str, str]]) -> None:
    audit_fields = [
        "pv_id",
        "pv",
        "v6_action",
        "v6_pool_status",
        "candidate_gate_status",
        "acceptable_item_id",
        "acceptable_sentence",
        "unacceptable_item_id",
        "unacceptable_sentence",
        "acceptable_word_count",
        "unacceptable_word_count",
        "word_count_delta_unacceptable_minus_acceptable",
        "acceptable_has_overt_cue",
        "unacceptable_has_overt_cue",
        "target_form_in_both",
        "acceptable_naturalness_1_4",
        "unacceptable_near_miss_1_4",
        "pv_dependency_1_4",
        "general_cue_risk_1_4",
        "alternate_sense_risk_1_4",
        "pair_rationale",
        "critical_note",
    ]
    write_tsv(PRE_AUDIO_AUDIT_V6, audit_rows, audit_fields)

    red_fields = [
        "pv_id",
        "pv",
        "v6_pool_status",
        "candidate_gate_status",
        "red_team_risk_level",
        "residual_risk_type",
        "red_team_note",
        "recommended_next_action",
    ]
    red_rows = []
    for row in audit_rows:
        note = RED_TEAM_NOTES[row["pv_id"]]
        if note["red_team_risk_level"] == "high":
            action = "revise_before_audio"
        elif row["v6_pool_status"] == "reserve_needs_native_review":
            action = "keep_as_reserve_only"
        else:
            action = "native_review_required"
        red_rows.append(
            {
                "pv_id": row["pv_id"],
                "pv": row["pv"],
                "v6_pool_status": row["v6_pool_status"],
                "candidate_gate_status": row["candidate_gate_status"],
                "recommended_next_action": action,
                **note,
            }
        )
    write_tsv(RED_TEAM_V6, red_rows, red_fields)

    candidate_counter = Counter(row["v6_pool_status"] for row in audit_rows)
    gate_counter = Counter(row["candidate_gate_status"] for row in audit_rows)
    red_counter = Counter(RED_TEAM_NOTES[row["pv_id"]]["red_team_risk_level"] for row in audit_rows)
    excluded_counter = Counter(
        row["v6_action"] for pv_id, row in feasibility.items() if pv_id not in CANDIDATE_PAIRS
    )
    active = [row for row in audit_rows if row["v6_pool_status"] == "active_candidate"]
    list_a_accept = sum(1 for i, _ in enumerate(active) if i % 2 == 0)
    list_a_unaccept = len(active) - list_a_accept

    lines = [
        "# LJT v6 candidate design summary v1",
        "",
        "## Status",
        "",
        "This is a pre-audio candidate set. It is not production-cleared and should not be recorded until native/expert review confirms semantic naturalness and PV dependency.",
        "",
        "## Design decisions",
        "",
        "- Use only targets rated `keep_revise_lightly` or `revise` in the v6 feasibility audit.",
        "- Do not force `replace_or_rewrite` or `drop` targets into the LJT.",
        "- Keep one additional weak candidate as a reserve rather than placing it in the balanced active lists.",
        "- Use same-domain near-misses to reduce broad noun-category cues.",
        "- Require native/expert review before audio generation.",
        "",
        "## Counts",
        "",
        f"- candidate PV pool: {len(audit_rows)}",
        f"- active balanced-list PVs: {len(active)}",
        f"- reserve candidates: {candidate_counter.get('reserve_needs_native_review', 0)}",
        f"- excluded or replacement-needed PVs: {len(feasibility) - len(audit_rows)}",
        "",
        "Candidate pool status:",
    ]
    for key, value in sorted(candidate_counter.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Preliminary gate status:"])
    for key, value in sorted(gate_counter.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Red-team residual risk:"])
    for key, value in sorted(red_counter.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Excluded target status:"])
    for key, value in sorted(excluded_counter.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## List balance",
            "",
            f"The active set has {len(active)} PVs. List A receives {list_a_accept} acceptable and {list_a_unaccept} unacceptable items; List B receives the opposite conditions. Each PV appears once per list.",
            "",
            "## Files",
            "",
            f"- `{ITEMS_V6.name}`: full 31-PV candidate pool, two rows per PV",
            f"- `{ASSIGNMENT_V6.name}`: 30-PV active balanced assignment",
            f"- `{LIST_A_V6.name}` and `{LIST_B_V6.name}`: pseudo-randomized active lists",
            f"- `{REVIEW_FORM_V6.name}`: expert-review form for all candidate items",
            f"- `{PRE_AUDIO_AUDIT_V6.name}`: item-level pre-audio gate audit",
            f"- `{RED_TEAM_V6.name}`: residual-risk review after the mechanical gate",
            f"- `{EXCLUDED_TARGETS_V6.name}`: targets requiring replacement, major rewrite, or drop",
        ]
    )
    SUMMARY_V6.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _, feasibility = load_inputs()
    missing = set(CANDIDATE_PAIRS) - set(feasibility)
    if missing:
        raise ValueError(f"Unknown PV IDs in candidate pairs: {sorted(missing)}")

    items, audit_rows, _ = make_items()
    make_review_form(items, audit_rows)
    make_lists(items)
    make_excluded(feasibility)
    make_audit_and_summary(audit_rows, feasibility)

    for path in [
        ITEMS_V6,
        ASSIGNMENT_V6,
        LIST_A_V6,
        LIST_B_V6,
        REVIEW_FORM_V6,
        PRE_AUDIO_AUDIT_V6,
        RED_TEAM_V6,
        EXCLUDED_TARGETS_V6,
        SUMMARY_V6,
    ]:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
